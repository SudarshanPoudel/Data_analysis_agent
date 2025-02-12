from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import json
from markdown_pdf import MarkdownPdf, Section

from src.utils.prompts import (
    REPORT_GENERATION_PROMPT_1,
    REPORT_GENERATION_PROMPT_2,
    REPORT_GENERATION_PROMPT_3,
)
from src.utils.llm import DEFAULT_LLM
from src.utils.helper import (
    parse_json_string,
    encode_markdown_image_urls,
    parse_markdown_string,
)
from src.agents import DataQueryAgent, ChartQueryAgent


class ReportAgent:
    """
    This is an Agent capable of generating report of entire dataset (csv, excel, json etc.) end to end.
    """

    def __init__(
        self, file_path: str, structure: str, llm=DEFAULT_LLM, verbose_level: int = 1
    ):
        self.path = file_path
        self.structure = structure
        self.llm = llm
        self.verbose = verbose_level

    def generate_report(self, save_report_as: str = None, save_plots_at: str = "Plots") -> dict:
        """
        This is the main method of this agent. It generates and saves a report for the given data file in three steps:
        
        1. Generate a general report overview: Give the LLM the structure of the dataset and ask it what the final report should look like.
        2. Based on the overview, generate questions for DataQueryAgent and ChartQueryAgent (code agents that generate responses and charts).
        3. Combine the overview and Q&A pairs to generate the final report.
        4. Optionally save the report as a PDF or Markdown file.

        Returns:
            dict: {
                "report_path": str | None,  # Path of the saved report (if applicable)
                "plots_path": str,  # Path where plots are saved
                "markdown": str  # Report content in markdown format
            }
        """

        self.report_overview = self._generate_report_overview()

        if self.verbose > 0:
            print(f"Report Overview Generated\n{self.report_overview}")

        self.questions = self._generate_questions(self.report_overview)

        if self.verbose > 1:
            print(f"\n\n--------\n\nQuestions to ask generated \n {self.questions}")

        self.qa_json = self._generate_qa_pair(
            self.questions, save_plots_at=save_plots_at
        )

        if self.verbose > 0:
            print(f"QA Pair generated\n{self.qa_json}")

        message_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(REPORT_GENERATION_PROMPT_3),
                HumanMessagePromptTemplate.from_template(
                    "Here is the json containing questions and answers related to dataset (step 2)\n ```json\n{qa_json}\n```"
                    "\n\n---\n\n"
                    "Final Report Overview:\n"
                    "{report_overview}"
                ),
            ]
        )
        message = message_template.format_messages(
            qa_json=self.qa_json, report_overview=self.report_overview
        )
        res = self.llm.invoke(message)
        markdown = encode_markdown_image_urls(parse_markdown_string(res.content))

        report_path = None  # Initialize report path

        if save_report_as:
            if save_report_as.endswith(".pdf"):
                pdf = MarkdownPdf(toc_level=2)
                css = "table {border-collapse: collapse; border-spacing: 0} table, th, td {border: 1px solid black;}"
                pdf.add_section(Section(markdown), user_css=css)
                pdf.save(save_report_as)
                report_path = save_report_as
            elif save_report_as.endswith(".md"):
                with open(save_report_as, "w") as f:
                    f.write(markdown)
                report_path = save_report_as
            else:
                raise ValueError(
                    "Unable to save report, it should be a valid string that ends with .md or .pdf"
                )

        return {
            "report_path": report_path,
            "plots_path": save_plots_at,
            "markdown": markdown,
        }


    def _generate_report_overview(self) -> str:
        """
        This is step 1 of this agent, it generates overall report overview
        """
        message = ChatPromptTemplate.from_messages(
            [
                SystemMessage(REPORT_GENERATION_PROMPT_1),
                HumanMessage(content=f"structure\n{self.structure}"),
            ]
        )
        res = self.llm.invoke(message.format())
        return res.content

    def _generate_questions(self, report_overview: str) -> dict:
        """
        This is step 2 of this agent, it generates questions to ask for data query agents and chart query agent.
        """
        message_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(REPORT_GENERATION_PROMPT_2),
                HumanMessagePromptTemplate.from_template(
                    "Here is the overall structure of the data\n {structure}"
                    "\n\n---\n\n"
                    "Final Report Would have:\n"
                    "{report_overview}"
                ),
            ]
        )
        message = message_template.format_messages(
            structure=self.structure, report_overview=report_overview
        )
        res = self.llm.invoke(message)
        return parse_json_string(res.content)

    def _generate_qa_pair(self, questions: dict, save_plots_at: str) -> str:
        """
        This is step 2.5, where we ask generated question to code agents and generate qa_pair.
        """
        data_agent = DataQueryAgent(
            file_path=self.path,
            structure=self.structure,
            verbose=self.verbose > 1,
        )
        graph_agent = ChartQueryAgent(
            file_path=self.path,
            structure=self.structure,
            save_plots_at=save_plots_at,
            verbose=self.verbose > 1,
        )

        question_answers = []

        for question in questions["DataQueryAgentQuestions"]:
            answer = data_agent.ask(question)
            question_answers.append({"question": question, "answer": answer["answer"]})

        for question in questions["ChartQueryAgentQuestions"]:
            answer = graph_agent.ask(question)
            question_answers.append(
                {
                    "question": question,
                    "answer": answer["answer"],
                    "charts": answer["charts"],
                }
            )
        return json.dumps(question_answers, indent=2)
