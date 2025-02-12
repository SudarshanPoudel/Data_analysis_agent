import os

from src.utils.models import GraphState
from src.agents.chart_query_agent import ChartQueryAgent


def chart_node(state: GraphState):
    """
    The chart node of the data analysis system.

    Args:
        state: The current graph state

    Returns:
        state: Updated state
    """
    print("====== CHART NODE ======")

    query = state["query"]
    path = state["data_path"]
    summary = state["data_summary"]

    # path conttains: c:/users/username/data/abc.csv and i need upto c:/users/username/data
    generation_path = os.path.dirname(path)
    save_plots_at = os.path.join(generation_path, "plots")

    chartAgent = ChartQueryAgent(
        file_path=path, structure=summary, save_plots_at=save_plots_at, verbose=False
    )

    res = chartAgent.ask(query)

    state["generation"] = res

    return {
        "generation": res,
    }
