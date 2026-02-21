"""Deterministic value parsing — no LLM needed here."""
import re


def parse_value(raw: str | int | float | None) -> float | None:
    """
    Convert raw cell values to float.
    Examples:
      "1,234.56" -> 1234.56
      "45%"      -> 0.45
      "YES"      -> 1.0
      "N/A"      -> None
      ""         -> None
    """
    if raw is None:
        return None

    value = str(raw).strip()

    if value.upper() in {"N/A", "NA", "NULL", "NONE", "-", "", "#N/A", "#VALUE!"}:
        return None

    if value.upper() in {"YES", "TRUE", "Y"}:
        return 1.0

    if value.upper() in {"NO", "FALSE", "N"}:
        return 0.0

    # Remove percentage sign — convert to decimal
    if value.endswith("%"):
        try:
            return float(value[:-1].replace(",", "")) / 100
        except ValueError:
            return None

    # Remove thousands separators and currency symbols
    cleaned = re.sub(r"[,$€£₹]", "", value).replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None


def validate_value(param_name: str, value: float | None) -> list[str]:
    """Return list of warning strings for suspicious values."""
    warnings = []
    if value is None:
        return warnings

    rules = {
        "efficiency": (0, 100),
        "plant_load_factor": (0, 100),
        "coal_consumption": (0, 50000),
        "co2_emissions": (0, 1_000_000),
    }

    if param_name in rules:
        lo, hi = rules[param_name]
        if not (lo <= value <= hi):
            warnings.append(
                f"Value {value} for '{param_name}' is outside expected range [{lo}, {hi}]"
            )

    if value < 0 and param_name not in {"heat_rate"}:
        warnings.append(f"Negative value {value} for '{param_name}' may be invalid")

    return warnings