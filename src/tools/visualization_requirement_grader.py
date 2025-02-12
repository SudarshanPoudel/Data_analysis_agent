from langchain_core.prompts import ChatPromptTemplate

from src.utils.models import GradeVisualizationRequirement
from src.utils.llm import DEFAULT_LLM

#### Defining the LLM ####
VISUALIZATION_REQUIREMENT_GRADER_LLM = DEFAULT_LLM

#### Defining the structured LLM grader which outputs a structured response ####
STRUCTURED_LLM_GRADER = VISUALIZATION_REQUIREMENT_GRADER_LLM.with_structured_output(
    GradeVisualizationRequirement
)

#### Defining prompts ####
VISUALIZATION_REQUIREMENT_GRADER_SYSTEM_PROMPT = """
You are a grader for a data analysis system tasked with evaluating user queries for relevance to data visualization. 
Given a summary of the available data and the user query:

1. Determine if the user query is specifically asking for a data visualization.
2. Provide a binary score:
   - "yes" if the query is relevant to requesting data visualization.
   - "no" if it is not.

Be precise and consistent in your evaluation. Only consider queries relevant to data visualization as "yes."
"""


VISUALIZATION_REQUIREMENT_GRADER_HUMAN_PROMPT = """
User query: 

```{query}```

Summary of the data: 

```{data_summary}```
"""

VISUALIZATION_REQUIREMENT_GRADER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", VISUALIZATION_REQUIREMENT_GRADER_SYSTEM_PROMPT),
        ("human", VISUALIZATION_REQUIREMENT_GRADER_HUMAN_PROMPT),
    ]
)

#### Exporting the retrieval grader chain ####
VISUALIZATION_REQUIREMENT_GRADER = (
    VISUALIZATION_REQUIREMENT_GRADER_PROMPT | STRUCTURED_LLM_GRADER
)
