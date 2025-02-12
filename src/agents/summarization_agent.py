import pandas as pd
import json
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate

from src.utils.llm import DEFAULT_LLM
from src.utils.prompts import (
    SUMMARIZATION_AGENT_SYSTEM_PROMPT,
    SUMMARIZATION_AGENT_USER_PROMPT,
)

class SummarizationAgent:
    def __init__(self, llm=DEFAULT_LLM):
        """
        This is the agent that extracts key metadata and Summarizes datasets.
        """
        self.llm = llm
        self.system_prompt = SUMMARIZATION_AGENT_SYSTEM_PROMPT
        self.user_prompt = SUMMARIZATION_AGENT_USER_PROMPT

    def summarize(self, file_path:str, metadata:str='')->str:
        """
        This methods returns summary of provided data. 
        """
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        elif file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        else:
            raise ValueError("Unsupported file format!")
        
        basic_info = {
            "total_rows": df.shape[0],
            "columns": []
        }

        for col in df.columns:
            example_values = df[col].dropna().head(5).tolist()
            # Check if the column is numerical
            if pd.api.types.is_numeric_dtype(df[col]):
                column_info = {
                    "column_name": col,
                    "data_type": str(df[col].dtype),
                    "range": f"{df[col].min()} to {df[col].max()}", 
                    "example_values": example_values or ['None'],
                    "null_values": str(df[col].isna().sum())
                }
            else:
                column_info = {
                    "column_name": col,
                    "data_type": str(df[col].dtype),
                    "unique_values": df[col].nunique(),
                    "example_values": example_values or ['None'],
                    "null_values": str(df[col].isna().sum())
                }
            basic_info["columns"].append(column_info)
            
        basic_json = json.dumps(basic_info, indent=4)
        message_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    self.system_prompt
                ),
                HumanMessagePromptTemplate.from_template(
                    self.user_prompt
                )
            ]
        )
        messages = message_template.format_messages(
           metadata=metadata,
           basic_json=basic_json
        )
        summary = self.llm.invoke(messages)
        return summary.content
