"""Track B: Parameter Onboarding Wizard API endpoints."""
import ast
import logging
import re

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.agents.parameter_suggester import suggest_parameters
from app.models.schemas import (
    AISuggestionRequest,
    AISuggestionResponse,
    FormulaValidationRequest,
    FormulaValidationResponse,
    OnboardingConfig,
)
from app.utils.registry import get_parameter_names, load_parameters

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/track-b", tags=["Track B: Onboarding Wizard"])

ALLOWED_FORMULA_TOKENS = re.compile(r"^[a-z0-9_\s\+\-\*\/\(\)\.\,]+$", re.IGNORECASE)


@router.get("/parameters", summary="Get parameter registry")
def get_parameters(asset_types: str = "") -> list[dict]:
    """
    Return parameter registry, optionally filtered by asset types.
    Query param: asset_types=boiler,turbine
    """
    params = load_parameters()
    if not asset_types:
        return params

    from app.utils.registry import load_assets

    requested_types = {t.strip().lower() for t in asset_types.split(",") if t.strip()}
    assets = load_assets()
    matching_assets = {a["name"] for a in assets if a["type"].lower() in requested_types}
    return [p for p in params if any(a in matching_assets for a in p.get("applicable_assets", []))]


@router.post("/validate-formula", response_model=FormulaValidationResponse)
def validate_formula(request: FormulaValidationRequest) -> FormulaValidationResponse:
    """
    Validate a formula expression.
    - Checks syntax is safe (no exec/eval injection)
    - Checks all referenced parameter names exist in the enabled set
    """
    expr = request.expression.strip()

    if not expr:
        return FormulaValidationResponse(valid=False, depends_on=[], missing_params=[], error="Empty expression")

    # Security: only allow safe characters
    if not ALLOWED_FORMULA_TOKENS.match(expr):
        return FormulaValidationResponse(
            valid=False, depends_on=[], missing_params=[], error="Formula contains invalid characters"
        )

    # Extract referenced parameter names (words that look like param names)
    all_param_names = set(get_parameter_names())
    tokens = re.findall(r"[a-z][a-z0-9_]*", expr, re.IGNORECASE)
    referenced = [t for t in tokens if t in all_param_names]
    missing = [t for t in referenced if t not in set(request.enabled_parameters)]

    # Try to parse as valid Python expression
    try:
        # Replace param names with 1.0 for syntax check
        test_expr = re.sub(r"[a-z][a-z0-9_]*", "1.0", expr, flags=re.IGNORECASE)
        ast.parse(test_expr, mode="eval")
    except SyntaxError as e:
        return FormulaValidationResponse(valid=False, depends_on=referenced, missing_params=missing, error=str(e))

    return FormulaValidationResponse(
        valid=len(missing) == 0,
        depends_on=referenced,
        missing_params=missing,
        error=f"Parameters not enabled: {missing}" if missing else None,
    )


@router.post("/suggest-parameters", response_model=AISuggestionResponse)
def suggest_params(request: AISuggestionRequest) -> AISuggestionResponse:
    """AI-powered parameter suggestion based on plant description."""
    return suggest_parameters(request)


@router.post("/onboarding", summary="Submit final onboarding config")
def submit_onboarding(config: OnboardingConfig) -> JSONResponse:
    """
    Accept the final plant configuration.
    In production this would persist to DB. For now, validates and echoes back.
    """
    logger.info(f"New plant onboarded: {config.plant.name}")
    return JSONResponse(
        content={
            "status": "success",
            "message": f"Plant '{config.plant.name}' successfully onboarded with "
                       f"{len(config.assets)} assets and {len(config.parameters)} parameters.",
            "config": config.model_dump(),
        }
    )