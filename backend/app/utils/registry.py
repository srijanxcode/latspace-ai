"""Loads and exposes the parameter and asset registries."""
import json
from pathlib import Path

REGISTRY_DIR = Path(__file__).parent.parent.parent / "registry"


def load_parameters() -> list[dict]:
    with open(REGISTRY_DIR / "parameters.json") as f:
        return json.load(f)


def load_assets() -> list[dict]:
    with open(REGISTRY_DIR / "assets.json") as f:
        return json.load(f)


def get_parameter_names() -> list[str]:
    return [p["name"] for p in load_parameters()]


def get_asset_names() -> list[str]:
    return [a["name"] for a in load_assets()]


def get_parameters_by_asset_types(asset_types: list[str]) -> list[dict]:
    """Filter parameters applicable to the given asset types."""
    assets = load_assets()
    asset_names_of_type = {a["name"] for a in assets if a["type"] in asset_types}
    params = load_parameters()
    return [
        p for p in params
        if any(a in asset_names_of_type for a in p.get("applicable_assets", []))
    ]