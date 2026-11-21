"""HTTP entry point: routes and app wiring."""

from fastapi import APIRouter, FastAPI

from app.schemas import AnalyzeRequest, AnalyzeResponse, Verdict

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(email: AnalyzeRequest) -> AnalyzeResponse:
    # Walking skeleton: no checks exist yet, so every email gets the empty result.
    return AnalyzeResponse(score=0, verdict=Verdict.SAFE, findings=[])


def create_app() -> FastAPI:
    app = FastAPI(title="Gmail Threat Scorer")
    app.include_router(router)
    return app


app = create_app()
