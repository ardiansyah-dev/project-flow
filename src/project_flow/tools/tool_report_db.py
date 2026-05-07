from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import mysql.connector
import os

class tool_report_dbInput(BaseModel):
    # Provide a very clear description to avoid confusion for the Agent
    head: int = Field(..., description="Number of heads without helmets (integer).")
    helmet: int = Field(..., description="Number of helmets detected (integer).")
    person: int = Field(..., description="Total number of people detected (integer).")

class tool_report_db(BaseTool):
    name: str = "tool_report_database" # Use snake_case for stability
    description: str = (
        "Use this tool to save helmet detection statistics to the database. "
        "Input MUST be three separate integer values: head, helmet, and person."
    )
    args_schema: Type[BaseModel] = tool_report_dbInput

    def _run(self, head: int, helmet: int, person: int) -> str:
        connection = None # Fix UnboundLocalError: Initialize connection variable
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )

            cursor = connection.cursor()
            
            # Logic: If there is a violation (head > 0)
            if head > 0:
                detail = f"{head} heads, {helmet} helmets, and {person} people"
                query = "INSERT INTO helmet_report (report_result, report_detected) VALUES (%s, %s)"
   
                cursor.execute(query, (detail, head))
                connection.commit()
                cursor.close()
                return f"FINAL ANSWER: Data successfully saved. {head} violations recorded."
            else:
                return "FINAL ANSWER: No violations detected. Task is complete and nothing was saved."

        except mysql.connector.Error as err:
            return f"Database Error: {err}"
        except Exception as e:
            return f"Unexpected Error: {e}"
        finally:
            # Fix UnboundLocalError: Check connection before closing
            if connection and connection.is_connected():
                connection.close()
