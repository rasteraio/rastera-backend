from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import AnalysisRequest, AnalysisResponse
from geoai.pipeline import build_pipeline

app = FastAPI(
    title="Rastera GeoAI Backend",
    version="0.1.0",
    description="Prototype GeoAI backend for Rastera – parses prompts and returns structured pipelines.",
)

# CORS settings – keep wide open for now; tighten later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["https://rastera.io"] once stable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "rastera-geoai-backend"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(req: AnalysisRequest):
    """
    Main entrypoint for Rastera:
    - Accepts a natural-language prompt and metadata
    - Returns a structured GeoAI pipeline + asset references
    """
    return build_pipeline(req)
