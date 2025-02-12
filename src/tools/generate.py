from langchain import hub
from langchain_core.output_parsers import StrOutputParser

from src.utils.llm import DEFAULT_LLM

#### Defining the LLM ####
GENERATOR_LLM = DEFAULT_LLM

#### Pulling the prompt ####
GENERATOR_PROMPT = hub.pull("rlm/rag-prompt")

#### Exporting the generator chain ####
GENERATOR_CHAIN = GENERATOR_PROMPT | GENERATOR_LLM | StrOutputParser()
