import os
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from ultralytics import YOLO

class tool_helmet_detectionInput(BaseModel):
    gambar: str = Field(..., description="The content of the file to be analyzed for helmet detection.")


class tool_helmet_detection(BaseTool):
    name: str = "Tool Helmet Detection"
    description: str = "Detects helmets in a given text file content. It returns a list of detected helmets."
    args_schema: Type[BaseModel] = tool_helmet_detectionInput
    modelYolo: YOLO = YOLO(os.path.join(os.path.dirname(__file__), 'modelyolobest.pt'))
    # modelYolo = YOLO(os.path.join(os.path.dirname(__file__), 'modelyolobest.pt')) 

    def _run(self, gambar: str) -> str:
        # Here you would implement the actual helmet detection logic.
        # For demonstration purposes, we'll return a dummy list of detected helmets.
        # In a real implementation, you might use libraries like OpenCV or machine learning models to detect helmets in images or videos.
        result = self.modelYolo.predict(gambar)
        detected_objects = result[0].boxes.cls.tolist() # type: ignore
        class_names =  result[0].names
        
        object_counts = {}
        head = 0
        helmet = 0
        person = 0

        for result in detected_objects:
          class_name = class_names[int(result)] # Get the class name from the dictionary

          if class_name == 'head':
            head += 1
          elif class_name == 'helmet':
            helmet += 1
          elif class_name == 'person':
            person += 1
        
        result_dict = {
            "result": f"Detected {person} person(s), {helmet} helmet(s), and {head} head(s) without helmets.",
            "head": head,
            "helmet": helmet,
            "person": person
        }

        print(str(result_dict))

        return str(result_dict)