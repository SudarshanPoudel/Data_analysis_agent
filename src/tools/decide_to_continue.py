from typing import Literal
from src.utils.models import GraphState


def decide_to_continue(state: GraphState) -> Literal["query_relevant", "query_not_relevant"]:
    """
    Determines whether to generate an answer(no answer) or to decide to visualize the data.

    Args:
        state: The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("====== ASSERT DATA RELEVANCE ======\n")

    related_to_data = state["related_to_data"]

    if related_to_data == "yes":
        # Check if visualization is required
        print("====== DECISION: DATA RELATED, CHECK IF VISUALIZATION REQUIRED ======\n")
        return "query_relevant"
    else:
        # The data is not related, so we need to transform the query
        print("====== DECISION: DATA NOT RELATED, END ======\n")
        return "query_not_relevant"
