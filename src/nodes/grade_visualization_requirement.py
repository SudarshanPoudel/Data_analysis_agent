from src.utils.models import GraphState
from src.tools.visualization_requirement_grader import VISUALIZATION_REQUIREMENT_GRADER


def grade_visualization_requirement(state: GraphState) -> GraphState:
    """
    Determines whether the provided user query requires visualization.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with requires_visualization key
    """
    print("====== CHECK VISUALIZATION REQUIREMENT ======")

    query = state["query"]
    data_summary = state["data_summary"]

    requires_visualization = "no"

    score = VISUALIZATION_REQUIREMENT_GRADER.invoke(
        {"query": query, "data_summary": data_summary}
    )
    grade = score.binary_score

    if grade == "yes":
        print("====== GRADE: USER QUERY REQUIRES VISUALIZATION ======")
        requires_visualization = "yes"
    else:
        print("====== GRADE: USER QUERY DOES NOT REQUIRE VISUALIZATION ======")

    state["requires_visualization"] = requires_visualization

    return state
