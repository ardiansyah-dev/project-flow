from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException, Response
import os
import uuid
from http import HTTPStatus
from pydantic import BaseModel
import tasks.celery_task as celeryTask
from celery.result import AsyncResult
from tasks.celery_app import celery_app

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