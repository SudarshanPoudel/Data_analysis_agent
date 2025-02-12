from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.utils.llm import DEFAULT_LLM

#### Defining the LLM ####
QUERY_REWRITER_LLM = DEFAULT_LLM

#### Defining prompts ####
QUERY_REWRITER_SYSTEM_PROMPT = """
You are a query re-writer that converts an input query to a better version that is optimized for understanding and processing.
Look at the input and try to reason about the underlying semantic intent / meaning.
"""

QUERY_REWRITER_HUMAN_PROMPT = """
Here is the initial query: 

```{query}```

Formulate an improved query.
"""

QUERY_REWRITER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", QUERY_REWRITER_SYSTEM_PROMPT),
        ("human", QUERY_REWRITER_HUMAN_PROMPT),
    ]
)

#### Exporting the query re-writer chain ####
QUERY_REWRITER = QUERY_REWRITER_PROMPT | QUERY_REWRITER_LLM | StrOutputParser()
