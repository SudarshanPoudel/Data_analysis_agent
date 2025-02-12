from src.utils.models import GraphState
from src.tools.user_query_grader import USER_QUERY_GRADER


def grade_query(state: GraphState) -> GraphState:
    """
    Determines whether the retrieved documents are relevant to the query.

    Args:
        state: The current graph state

    Returns:
        state: Updated state with related_to_data key
    """
    print("====== CHECK USER QUERY RELEVANCE ======")

    query = state["query"]
    data_summary = state["data_summary"]

    related_to_data = "yes"

    score = USER_QUERY_GRADER.invoke({"query": query, "data_summary": data_summary})
    grade = score.binary_score

    if grade == "yes":
        print("====== GRADE: USER QUERY RELEVANT ======")
    else:
        print("====== GRADE: USER QUERY NOT RELEVANT ======")
        related_to_data = "no"

    state["related_to_data"] = related_to_data

    return state
