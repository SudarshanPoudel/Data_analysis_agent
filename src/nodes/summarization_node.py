from src.utils.models import GraphState
from src.config.db import initialize_db
from src.agents.summarization_agent import SummarizationAgent
from src.tools.summary import store_summary_in_db, get_summary_from_db


def summarization_node(state: GraphState) -> GraphState:
    """
    The summarization node of the data analysis system.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with summary key
    """
    print("====== SUMMARIZATION NODE ======")

    path = state["data_path"]
    metadata = state["metadata"]

    # Initialize the database
    initialize_db()

    # Check if summary already exists
    summary = get_summary_from_db(path)
    if summary is None:
        print(f"No existing summary found for {path}. Generating new summary...")
        summary = SummarizationAgent().summarize(file_path=path, metadata=metadata)
        store_summary_in_db(path, summary)
    else:
        print(f"Using cached summary for {path}.")

    state["data_summary"] = summary

    return state
