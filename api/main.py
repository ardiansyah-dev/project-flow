from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Response
import os
import uuid
from http import HTTPStatus
from pydantic import BaseModel
import tasks.celery_task as celeryTask
from celery.result import AsyncResult
from tasks.celery_app import celery_app
import shutil

TEXT_FOLDER = "files_test" 
os.makedirs(TEXT_FOLDER, exist_ok=True)

app = FastAPI()

class ResearchInput(BaseModel):
  topic: str

class MarketResearchInput(BaseModel):
  topic: str
  location: str
  year: int

class SystemAnalystInput(BaseModel):
  topic: str
  style: str

class DeveloperInput(BaseModel):
  topic: str
  language: str

@app.post("/research")
async def research(researchInput: ResearchInput):
  task = celeryTask.research.delay(researchInput.topic) # type: ignore
  return {"task_id": task.id}

@app.post("/market-research")
async def market_research(marketResearchInput: MarketResearchInput):
  task = celeryTask.market_research.delay(marketResearchInput.topic, marketResearchInput.location, marketResearchInput.year) # type: ignore
  return {"task_id": task.id}

@app.post("/system-analyst")
async def system_analysis(systemAnalystInput: SystemAnalystInput):
  task = celeryTask.system_analysis.delay(systemAnalystInput.topic, systemAnalystInput.style) # type: ignore
  return {"task_id": task.id}

@app.post("/developer")
async def developer(developerInput: DeveloperInput):
  task = celeryTask.developer_crew.delay(developerInput.topic, developerInput.language) # type: ignore
  return {"task_id": task.id}

@app.post("/file-analyzer")
async def file_analyzer(file: UploadFile=File(...)):
  if file.content_type != "text/plain":
    raise HTTPException(status_code=400,detail="File must be a TXT")

  _, file_extension = os.path.splitext(file.filename or "file")
  file_extension = file_extension or ".txt"
  unique_filename = f"{uuid.uuid4().hex}{file_extension}"
  file_path = os.path.join(TEXT_FOLDER, unique_filename)

  #  Save the file
  content = await file.read()
  with open(file_path, "wb") as f:
    f.write(content)

  task = celeryTask.file_analyzer.delay(file_path) # type: ignore
  return {"task_id": task.id, "file_path": file_path}

@app.post("/anomaly-detection")
async def anomaly_detection(file: UploadFile=File(...)):
  if not file.filename or file.filename.endswith(('.xlsx', '.xls')):
    raise HTTPException(status_code=400,detail="File must be a XLSX")

  file_extension = os.path.splitext(file.filename)[1] or ".xlsx"
  unique_filename = f"{uuid.uuid4().hex}{file_extension}"
  file_path = os.path.join(TEXT_FOLDER, unique_filename)
  absolute_file_path = os.path.abspath(file_path)

  try:
    #  Save the file
    content = await file.read()
    with open(file_path, "wb") as f:
      f.write(content)

    task = celeryTask.anomaly_detection.delay(file_name=file.filename, file_path=absolute_file_path) # type: ignore
    return {"task_id": task.id, "file_path": absolute_file_path, "file_name": file.filename}
  except Exception as e:
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Failed to save the file: {str(e)}")


@app.get("/status/{task_id}")
async def get_status(task_id:str):
  task_result = AsyncResult(task_id, app=celery_app)

  response = {
    "task_id": task_id,
    "status": task_result.state,
    "result": None,
    "error": None
  }

  if task_result.state == 'SUCCESS':
    response["result"] = task_result.result
  if task_result.state == 'FAILURE':
    response['error'] = str(task_result.info)
  
  return response

# @app.post("/market-research")
# async def market_research(researchInput: ResearchInput):
#   task = celeryTask.market_research.delay(researchInput.topic) # type: ignore
#   return {"task_id": task.id}