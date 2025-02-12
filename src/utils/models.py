from typing import Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


#### Application graph data model state ####
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        query: str
        data_summary: str
        related_to_data: bool
        requires_visualization: bool
        generation: str
        report: str
        data_path: str
        metadata: str
    """

    query: str | None
    data_summary: str | None
    related_to_data: Literal["yes", "no"] | None
    requires_visualization: Literal["yes", "no"] | None
    generation: str | None
    report: Literal["yes", "no"] | None
    data_path: str | None
    metadata: str | None


#### Model for retrieval grading output structure ####
class GradeGeneration(BaseModel):
    """Binary score for relevance check on generated output."""

    binary_score: str = Field(
        description="Generated output is relevant to user query, 'yes' or 'no'"
    )


#### Model for visualization requirement grading output structure ####
class GradeVisualizationRequirement(BaseModel):
    """Binary score for visualization requirement check."""

    binary_score: str = Field(
        description="User query requires visualization, 'yes' or 'no'"
    )


#### Model for user query grading output structure ####
class GradeUserQuery(BaseModel):
    """Binary score for user query relevance check."""

    binary_score: str = Field(
        description="User query is relevant to the data, 'yes' or 'no'"
    )
