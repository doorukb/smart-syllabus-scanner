from __future__ import annotations
from pydantic import BaseModel, Field
from demo_extract import SyllabusExtraction, ValidationResult, PolicyFlagResult

class ExtractionResponse(BaseModel):
    extraction: SyllabusExtraction
    validation: ValidationResult
    policy_flags: PolicyFlagResult


class TextRequest(BaseModel):
    text: str = Field(..., description="Raw syllabus text to extract from")
    export_calendar: bool = Field(
        default=False,
        description="If true, include a base64-encoded .ics file in the response",
    )

class HealthResponse(BaseModel):
    status: str
    version: str

class InfoResponse(BaseModel):
    name: str
    description: str
    endpoints: list[str]