"""AI agent for suggesting parameters based on plant description (Track B stretch goal)."""
import json
import os
import re

import google.generativeai as genai

from app.models.schemas import AISuggestionRequest, AISuggestionResponse
from app.utils.registry import load_parameters

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def suggest_parameters(request: AISuggestionRequest) -> AISuggestionResponse:
    """Use Gemini to suggest relevant parameters for a plant."""
    params = load_parameters()
    param_list = json.dumps(
        [{"name": p["name"], "display_name": p["display_name"], "section": p["section"]} for p in params],
        indent=2,
    )

    prompt = f"""You are an industrial ESG consultant helping configure a factory monitoring system.

A new plant is being onboarded with:
- Description: {request.plant_description}
- Asset types present: {', '.join(request.asset_types)}

Available parameters:
{param_list}

Based on the plant description and asset types, suggest which parameters are MOST RELEVANT to enable.
Consider: what equipment is present, what energy sources are likely, what emissions to track.

Return ONLY valid JSON (no markdown):
{{
  "suggested_parameter_names": ["coal_consumption", "steam_generation", ...],
  "reasoning": "Brief explanation of why these parameters were selected"
}}"""

    model = genai.GenerativeModel(MODEL)
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json",
            ),
        )
        raw = response.text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
        return AISuggestionResponse(**data)
    except Exception as e:
        return AISuggestionResponse(
            suggested_parameter_names=[p["name"] for p in params],
            reasoning=f"Could not generate AI suggestion: {e}. Showing all parameters.",
        )