from typing import Literal
from src.utils.models import GraphState


def decide_to_report(state: GraphState) -> Literal["report", "no_report"]:
    """
    Determines whether to route to the report node or not.

    Args:
        state: The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("====== CHECK IF REPORT OR NO REPORT ======\n")

    report = state["report"]

    if report == "yes":
        print("====== DECISION: REPORT GENERATION REQUIRED ======\n")
        return "report"
    else:
        print("====== DECISION: NO REPORT REQUIRED ======\n")
        return "no_report"
