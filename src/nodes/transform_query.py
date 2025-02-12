from src.utils.models import GraphState
from src.tools.query_rewriter import QUERY_REWRITER


def transform_query(state: GraphState) -> GraphState:
    """
    Transform the query to produce a better question.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with the transformed question
    """
    print("====== TRANSFORM QUERY ======")

    query = state["query"]
    better_query = QUERY_REWRITER.invoke({"query": query})

    # remove the quotes from the better question
    better_query = better_query.replace('"', "")

    # Update the question
    state["query"] = better_query

    return state
