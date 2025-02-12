from typing import Literal
from src.utils.models import GraphState


def decide_to_visualize(state: GraphState) -> Literal["not_visualize", "visualize"]:
    """
    Determines whether to visualize the data.

    Args:
        state: The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("====== DECIDE TO VISUALIZE ======")

    requires_visualization = state["requires_visualization"]

    if requires_visualization == "yes":
        # Check if visualization is required
        print("====== DECISION: VISUALIZATION REQUIRED ======\n")
        return "visualize"
    else:
        print("====== DECISION: NO VISUALIZATION REQUIRED ======\n")
        return "not_visualize"
