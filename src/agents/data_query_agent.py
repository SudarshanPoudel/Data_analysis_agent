from src.utils.prompts import DATA_QUERY_AGENT_SYSTEM_PROMPT, DEFAULT_USER_PROMPT
from src.utils.llm import DEFAULT_LLM
from src.utils.additional_source_code import get_additional_code
from src.agents.code_agent import CodeAgent

class DataQueryAgent(CodeAgent):
    def __init__(
        self, 
        file_path:str,
        structure:str,
        llm = DEFAULT_LLM,
        max_iter:int = 10,
        verbose: bool = True
    ):
        """
        This is the child class of code agent capable of deciding which chart to make, generating code for plot, executing and debugging code. 

        Args:
            file_path: Path of data file
            structure: Extracted structure with metadata of dataset
            llm: LLM to use for our agent, supports any langchain Chat Agents
            max_iter: Maximum number of LLM calls that we can do to solve one task
            verbose: Bool to decide whether or not print intermediate results.
        """
        super().__init__(
            file_path=file_path,
            structure=structure,
            system_prompt=DATA_QUERY_AGENT_SYSTEM_PROMPT,
            user_prompt=DEFAULT_USER_PROMPT,
            llm=llm,
            additional_imports=['pandas', 'tabulate'],
            additional_code=get_additional_code('DataQueryAgent'),
            verbose=verbose,
            max_iter=max_iter
        )