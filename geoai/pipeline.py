from typing import List, Optional

from models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    PipelineStep,
    AssetReference,
)


def infer_task_type(prompt: str, fallback: Optional[str] = None) -> str:
    p = prompt.lower()
    if "flood" in p:
        return "flood-risk"
    if "shoreline" in p or "coast" in p or "erosion" in p:
        return "coastal-change"
    if "wildfire" in p or "fire" in p:
        return "wildfire-risk"
    if "land-use" in p or "land use" in p or "lulc" in p:
        return "land-use-change"
    return fallback or "generic-geoai"


def build_pipeline(req: AnalysisRequest) -> AnalysisResponse:
    task_type = req.task_type or infer_task_type(req.prompt)

    steps: List[PipelineStep] = [
        PipelineStep(
            order=1,
            name="Parse request",
            description=(
                "Extract study area, time window, hazards, and desired outputs from the natural-language prompt."
            ),
        ),
        PipelineStep(
            order=2,
            name="Discover datasets",
            description=(
                "Search STAC catalogs (e.g., Planetary Computer, local STAC) for DEM, land-use, and hazard rasters "
                "matching the study area and time window."
            ),
        ),
        PipelineStep(
            order=3,
            name="Prepare rasters",
            description=(
                "Reproject rasters to a common CRS, align pixel grids, clip to the study area, and handle nodata values."
            ),
        ),
        PipelineStep(
            order=4,
            name="Run GeoAI workflow",
            description=(
                f"Apply task-specific pipeline for '{task_type}' "
                "(e.g., flood depth overlay, shoreline change detection, or land-use change matrix)."
            ),
        ),
        PipelineStep(
            order=5,
            name="Aggregate & score",
            description=(
                "Aggregate raster outputs to parcels, grids, or sub-watersheds and compute risk/suitability scores."
            ),
        ),
        PipelineStep(
            order=6,
            name="Export outputs",
            description=(
                "Export GeoTIFFs, vector layers, and ready-to-use map tiles or PDFs for visualization and reporting."
            ),
        ),
    ]

    # Dummy asset references for now – later you’ll plug in real URIs
    assets: List[AssetReference] = [
        AssetReference(
            type="geotiff",
            uri="s3://rastera-demo/jobs/example_flood_depth.tif",
            metadata={
                "description": "Flood depth raster (demo URI)",
                "crs": "EPSG:3857",
            },
        ),
        AssetReference(
            type="geopackage",
            uri="s3://rastera-demo/jobs/example_parcels.gpkg",
            metadata={"description": "Parcel-level risk scores (demo URI)"},
        ),
    ]

    narrative = (
        f"For the task '{task_type}', Rastera constructs a GeoAI workflow that discovers appropriate rasters, "
        f"preprocesses them into a consistent analysis grid, runs task-specific models or overlays, and aggregates "
        f"the results into decision-ready layers. This response is a prototype; wire it to your actual raster engine "
        f"and storage to make it fully operational."
    )

    return AnalysisResponse(
        prompt=req.prompt,
        study_area=req.study_area,
        time_window=req.time_window,
        task_type=task_type,
        pipeline=steps,
        assets=assets,
        narrative=narrative,
    )
