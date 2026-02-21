"""Pydantic models for structured LLM output and API responses."""
from pydantic import BaseModel, Field
from typing import Optional


# ── Track A ────────────────────────────────────────────────────────────────

class ColumnMapping(BaseModel):
    col_index: int
    original_header: str
    param_name: Optional[str] = None
    asset_name: Optional[str] = None
    confidence: str = Field(default="low", pattern="^(high|medium|low)$")
    reasoning: str = ""


class LLMMappingResponse(BaseModel):
    """Structured output expected from the Gemini mapping call."""
    mappings: list[ColumnMapping]
    unmapped_headers: list[str] = []
    header_row_index: int = 0
    notes: str = ""


class ParsedCell(BaseModel):
    row: int
    col: int
    param_name: str
    asset_name: Optional[str] = None
    raw_value: str
    parsed_value: Optional[float]
    confidence: str


class UnmappedColumn(BaseModel):
    col: int
    header: str
    reason: str


class ParseResponse(BaseModel):
    status: str
    header_row: int
    parsed_data: list[ParsedCell]
    unmapped_columns: list[UnmappedColumn]
    warnings: list[str]
    duplicate_flags: list[str] = []


# ── Track B ────────────────────────────────────────────────────────────────

class PlantInfo(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    manager_email: str


class AssetConfig(BaseModel):
    name: str
    display_name: str
    type: str


class ParameterConfig(BaseModel):
    name: str
    display_name: str
    unit: str
    category: str
    section: str
    applicable_assets: list[str]


class FormulaConfig(BaseModel):
    parameter: str
    expression: str
    depends_on: list[str]


class OnboardingConfig(BaseModel):
    plant: PlantInfo
    assets: list[AssetConfig]
    parameters: list[ParameterConfig]
    formulas: list[FormulaConfig]


class FormulaValidationRequest(BaseModel):
    expression: str
    enabled_parameters: list[str]


class FormulaValidationResponse(BaseModel):
    valid: bool
    depends_on: list[str]
    missing_params: list[str]
    error: Optional[str] = None


class AISuggestionRequest(BaseModel):
    plant_description: str
    asset_types: list[str]


class AISuggestionResponse(BaseModel):
    suggested_parameter_names: list[str]
    reasoning: str