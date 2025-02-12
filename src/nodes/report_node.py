from src.utils.models import GraphState
from src.agents.report_agent import ReportAgent
import os
import shutil

def report_node(state: GraphState):
    """
    The report node of the data analysis system.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with generation key
    """
    print("====== REPORT NODE ======")

    path = state["data_path"]
    summary = state["data_summary"]

    report_agent = ReportAgent(
        file_path=path, 
        structure=summary, 
        verbose_level=0
    )
    report_dir = "data/report"

    # Delete the folder if it exists
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)

    filename = os.path.splitext(os.path.basename(path))[0]
    res = report_agent.generate_report(save_report_as=f"data/report/{filename}-report.pdf", save_plots_at="data/report/plots")

    state["generation"] = res

    return {
        "generation": res,
    }
