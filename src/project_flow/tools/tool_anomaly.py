from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import pandas as pd
from sklearn.ensemble import IsolationForest

class tool_anomalyInput(BaseModel):
    file: str = Field(..., description="The content of the file to be analyzed for anomalies.")

class tool_anomalyOutput(BaseModel):
    anomalies: list[str] = Field(..., description="List of detected anomalies in the file.")

class ToolAnomaly(BaseTool):
    name: str = "Tool Anomaly Detection"
    description: str = "Detects anomalies in a given text file content. It returns a list of detected anomalies."
    args_schema: Type[BaseModel] = tool_anomalyInput

    def _run(self, file: str) -> tool_anomalyOutput:
        # Here you would implement the actual anomaly detection logic.
        # For demonstration purposes, we'll return a dummy list of anomalies.
        # In a real implementation, you might use libraries like pandas, numpy, or even machine learning models to detect anomalies in the text.


        df = pd.read_excel(file, sheet_name=0)
        df = df.iloc[:,1:]

        for col in df.select_dtypes(include=['object']).columns:
          df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df_clean = df.dropna()
        df_clean['day_number'] = (df_clean['time'] - pd.Timestamp('2000-01-01')).dt.days
        df_fix = df_clean.iloc[:,1:]

        iso_forest = IsolationForest(
          contamination=0.05,
          random_state=42,
          n_estimators=100
        )
        iso_forest.fit(df_fix)

        if 'anomaly' in df_fix.columns:
          df_fix = df_fix.drop('anomaly', axis=1)
        df_fix['anomaly'] = iso_forest.predict(df_fix)

        anomaly_count = (df_fix['anomaly'] == -1).sum()
        total_data = len(df_fix)
        
        print(f"Anomaly count: {anomaly_count}", f"Total data points: {total_data}")
        
        # dataReturn = {
        #     "anomaly_count": int(anomaly_count),
        #     "total_data": int(total_data),
        # }
        return tool_anomalyOutput(anomalies=[f"Anomaly count: {anomaly_count}", f"Total data points: {total_data}"])
