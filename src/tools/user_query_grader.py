from langchain_core.prompts import ChatPromptTemplate
from src.utils.models import GradeUserQuery

from src.utils.llm import DEFAULT_LLM

#### Defining the LLM ####
USER_QUERY_GRADER_LLM = DEFAULT_LLM

#### Defining the structured LLM grader which outputs a structured response ####
STRUCTURED_LLM_GRADER = USER_QUERY_GRADER_LLM.with_structured_output(GradeUserQuery)

#### Defining prompts ####
USER_QUERY_GRADER_SYSTEM_PROMPT = """
You are a grader for a data analysis system tasked with evaluating user queries for relevance to data. 
Given a summary of the available data and the user query:

1. Determine if the user query is specifically asking about the data or related topics.
2. Provide a binary score:
   - "yes" if the query is relevant to the data.
   - "no" if it is not.

Focus on assessing whether the query directly pertains to data-related topics, including access, analysis, or interpretation.
"""


USER_QUERY_GRADER_HUMAN_PROMPT = """
User query: 

```{query}```

Summary of the data: 

```{data_summary}```
"""

USER_QUERY_GRADER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", USER_QUERY_GRADER_SYSTEM_PROMPT),
        ("human", USER_QUERY_GRADER_HUMAN_PROMPT),
    ]
)

#### Exporting the retrieval grader chain ####
USER_QUERY_GRADER = USER_QUERY_GRADER_PROMPT | STRUCTURED_LLM_GRADER
