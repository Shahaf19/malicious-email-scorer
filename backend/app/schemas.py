"""Request and response contract for POST /analyze.

Every request field is attacker-controlled email content, so the request model accepts
exactly the documented fields and types.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

MIN_SCORE = 0
MAX_SCORE = 100


class _StrictInput(BaseModel):
    # Unknown fields and type coercion ("5" -> 5) are rejected rather than tolerated, so the
    # only input that reaches analysis is input we have described and tested.
    model_config = ConfigDict(extra="forbid", strict=True)


class AnalyzeRequest(_StrictInput):
    headers: str = Field(min_length=1)
    subject: str
    body_text: str
    body_html: str


class Verdict(StrEnum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"


class Finding(BaseModel):
    id: str
    title: str
    detail: str
    points: int


class AnalyzeResponse(BaseModel):
    score: int = Field(ge=MIN_SCORE, le=MAX_SCORE)
    verdict: Verdict
    findings: list[Finding]
