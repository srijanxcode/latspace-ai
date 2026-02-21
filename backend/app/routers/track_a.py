"""Track A: Excel Parser API endpoints."""
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.agents.excel_parser import parse_excel
from app.models.schemas import ParseResponse

router = APIRouter(prefix="/api/track-a", tags=["Track A: Excel Parser"])


@router.post("/parse", response_model=ParseResponse, summary="Parse an Excel file")
async def parse_excel_file(file: UploadFile = File(...)) -> ParseResponse:
    """
    Upload an .xlsx file and get back structured, validated JSON.

    - Detects header rows automatically
    - Maps messy column names to canonical parameters using AI
    - Detects asset references in column headers
    - Parses and validates all numeric values
    - Flags unmapped columns, duplicates, and suspicious values
    """
    if not file.filename or not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported.")

    contents = await file.read()
    if len(contents) > 20 * 1024 * 1024:  # 20MB limit
        raise HTTPException(status_code=413, detail="File too large. Max 20MB.")

    try:
        result = parse_excel(contents, file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")