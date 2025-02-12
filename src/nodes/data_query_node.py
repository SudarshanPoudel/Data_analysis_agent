from src.utils.models import GraphState
from src.agents.data_query_agent import DataQueryAgent


def data_query_node(state: GraphState):
    """
    The node of the data analysis system which performs code analysis.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with generation key
    """
    print("====== DATA QUERY NODE ======")

    path = state["data_path"]
    summary = state["data_summary"]
    query = state["query"]

    data_query_agent = DataQueryAgent(
        file_path=path,
        structure=summary,
        verbose=False
    )
    res = data_query_agent.ask(query)

    state["generation"] = res
    
    print("Generation:")
    print(res)  

    return {
        "generation": res,
    }
