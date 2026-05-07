from tasks.celery_app import celery_app
from src.project_flow.crews.content_crew.content_crew import ContentCrew
from src.project_flow.crews.analisator.analisator import Analisator
from src.project_flow.crews.system_analyst.system_analyst import SystemAnalyst
from src.project_flow.crews.developer_crew.developer_crew import DeveloperCrew
from src.project_flow.crews.file_analyzer.file_analyzer import FileAnalyzer
from src.project_flow.crews.helmet_detector.helmet_detector import HelmetDetector
from src.project_flow.crews.anomaly.anomaly import Anomaly
import logging
import traceback
import json

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="research")
def research(self, topic:str):
    self.update_state(state="RUNNING", meta="current:"f"start job for {topic}")
    try:
        result = ContentCrew().crew().kickoff(inputs={"topic":topic})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="market_research")
def market_research(self, topic:str,location:str,year:int):
    self.update_state(state="RUNNING", meta="current:"f"start job for {topic} in {location} at {year}")
    try:
        result = Analisator().crew().kickoff(inputs={"topic":topic, "location":location, "year":year})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="system_analysis")
def system_analysis(self, topic: str, style: str):
    self.update_state(state="RUNNING", meta="current:"f"start system analysis for {topic} with requirements {style}")
    try:
        result = SystemAnalyst().crew().kickoff(inputs={"topic": topic, "style": style})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="developer_crew")
def developer_crew(self, topic:str, language:str):
    self.update_state(state="RUNNING", meta="current:"f"start developer for {topic} with language {language}")
    try:
        result = DeveloperCrew().crew().kickoff(inputs={"topic": topic, "language": language})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="file_analyzer")
def file_analyzer(self, file:str):
    self.update_state(state="RUNNING", meta="current:"f"start file analysis for {file}")
    try:
        result = FileAnalyzer().crew().kickoff(inputs={"file": file})
        # return str(result)
        return result.to_dict() # type: ignore
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="anomaly_detection")
def anomaly_detection(self, file_name:str, file_path:str):
    self.update_state(state="RUNNING", meta="current:"f"start anomaly detection for {file_name} at {file_path}")
    try:
        result = Anomaly().crew().kickoff(inputs={"file_name": file_name, "file_path": file_path})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise

@celery_app.task(bind=True, name="helmet_detection")
def helmet_detection(self, gambar:str):
    self.update_state(state="RUNNING", meta="current:"f"start helmet detection for {gambar}")
    try:
        result = HelmetDetector().crew().kickoff(inputs={"gambar": gambar})
        return str(result)
    except Exception as e:
        logger.error(f"Task failed with error: {e}\n{traceback.format_exc()}")
        raise