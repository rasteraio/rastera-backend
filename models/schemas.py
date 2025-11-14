from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AnalysisRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Natural-language description of the analysis, e.g., 'Map sunny-day flood risk for New Hanover County, NC using 1 m DEM and 0.5 m sea-level rise.'",
    )
    study_area: Optional[str] = Field(
        None,
        description="Study area name or code, e.g., 'Arlington County, VA' or an ISO/county code.",
    )
    time_window: Optional[str] = Field(
        None,
        description="Time period, e.g., '2018–2024' or 'current + 2050'.",
    )
    task_type: Optional[str] = Field(
        None,
        description="Optional task hint like 'flood-risk', 'land-use-change', 'wildfire', etc.",
    )


class PipelineStep(BaseModel):
    order: int
    name: str
    description: str


class AssetReference(BaseModel):
    type: str  # e.g. 'geotiff', 'cog', 'geopackage', 'tilejson'
    uri: str
    metadata: Dict[str, Any] = {}


class AnalysisResponse(BaseModel):
    prompt: str
    study_area: Optional[str]
    time_window: Optional[str]
    task_type: Optional[str]
    pipeline: List[PipelineStep]
    assets: List[AssetReference]
    narrative: str
