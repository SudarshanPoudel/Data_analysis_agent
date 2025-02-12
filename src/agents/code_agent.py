import re
import time
from typing import List
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from google.api_core.exceptions import ResourceExhausted

from src.utils.helper import parse_code_blobs
from src.utils.prompts import DEFAULT_USER_PROMPT
from src.utils.llm import DEFAULT_LLM
from src.utils.e2b_executor import E2BExecutor
from src.utils.logging import print_code_agents_logs


class CodeAgent:
    def __init__(
        self,
        file_path: str,
        structure: str,
        system_prompt: str,
        user_prompt=DEFAULT_USER_PROMPT,
        llm=DEFAULT_LLM,
        additional_imports: List[str] = [],
        additional_code: str = "",
        max_iter: int = 10,
        verbose=True,
        save_plots_at: str = None,
    ):
        """
        This is the class for agent capable of generating, executing and debugging code.
        We can be make changes in system prompt according to how we want our agent to act.

        Args:
            file_path: Path of data file
            structure: Extracted structure with metadata of dataset
            system_prompt: System prompt for our agent to use
            user_prompt: Initial prompt to given from user side
            llm: LLM to use for our agent, supports any langchain Chat Agents
            additional_imports: Any additional libraries that we let our agent to install and use in sandbox
            additional_code: Any additional python code to append before every llm generated code
            max_iter: Maximum number of LLM calls that we can do to solve one 
            save_charts_at: Folder path to save plots if code generates any
        """
        self.file_path = file_path
        self.structure = structure
        self.llm = llm
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.max_iter = max_iter
        self.additional_code = additional_code
        self.verbose = verbose
        
        self.executor = E2BExecutor(
            additional_imports=additional_imports,
            additional_files=[file_path],
            save_plots_at=save_plots_at,
        )

    def ask(self, query, **prompt_kwargs):
        """
        This method starts the code generation, refinement, and observation cycle with LLM.
        Additional arguments for prompt customization can be passed via prompt_kwargs.
        """
        init_message_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    self.system_prompt
                ),
                HumanMessagePromptTemplate.from_template(
                    self.user_prompt
                )
            ]
        )

        # Merge the standard arguments with any additional prompt_kwargs
        messages = init_message_template.format_messages(
            query=query, 
            file_path=self.file_path, 
            structure=self.structure, 
            **prompt_kwargs  
        )
        
        generated_charts = []
        for i in range(self.max_iter):  
            single_call = self._ask_singe(messages)

            if self.verbose:
                print_code_agents_logs(i + 1, single_call, query) 
            
            if single_call['is_final']:
                return {
                    'answer': single_call['output'],
                    'charts': list(set(generated_charts + single_call['charts']))
                }
            else:
                iteration_result = single_call['output']
                iteration_result += f"\n-----\n\nRemember user's original query is : {query}, if above response answers it, reprint response in final_answer(), else generate next iteration of code"
                if len(single_call['llm_response'].content) > 0:
                    new_messages = [
                        single_call['llm_response'], 
                        HumanMessage(content=iteration_result)
                    ]
                else:
                    new_messages = [
                        HumanMessage(content=iteration_result)
                    ]
                messages += new_messages
                generated_charts = list(set(generated_charts + single_call['charts']))

        return {
            'answer': f"Sorry, I'm unable to answer your question within {self.max_iter} iterations, either due to the complexity of your query or I was unable to debug errors.",
            'charts': []
        }
    

    def _ask_singe(self, messages):
        """
        This method does a single LLM called based upon provided messages list, based on returned response:
        - It extracts code blobs
        - Decides whether or not code need to be executed in Sandbox, if so execute it.
        - Decides whether or not further call is necessary or this is the final response.
        """
        retry_after = 10 
        while True:
            try:
                llm_response = self.llm.invoke(messages)  
                break  
            except ResourceExhausted:
                print(f"LLM Resource exhausted. Retrying in {retry_after} seconds...")
                time.sleep(retry_after)  
                retry_after *= 2
                if retry_after > 320:
                    raise
        
        try:
            llm_code =  parse_code_blobs(llm_response.content)
        except ValueError as e:
            return {
                'llm_response': llm_response,
                'output': str(e),
                'charts': [],
                'is_final': False
            }
        
        if len(self.additional_code) > 0:
            code = self.additional_code + "\n" + llm_code
        execution_result = self.executor.run(code)
        
        # Test if it's final execution and code had no error
        is_final = 'final_answer(' in llm_code  and execution_result['error'] is None

        if is_final and 'print(' in llm_code: 
            is_final = False
            execution_result['output'] += "\n\nIt seems like you're trying to give final answer and printing other values as well, don't do that. Call final_answer() again based on above response without any extra print() function calls, not even in try except block."
        
        return {
            'llm_response': llm_response,
            'output': execution_result['output'] or execution_result['error'] or 'Error occurred while executing code, and unable to detect reason.',
            'charts': execution_result['charts'],
            'is_final': is_final
        }
