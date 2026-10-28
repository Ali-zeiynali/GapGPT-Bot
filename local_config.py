"""Read local credentials without keeping account secrets in source control."""
import json
import os
from pathlib import Path


def get_setting(name: str, *, fallback: str | None = None) -> str:
    path = Path(__file__).with_name("credentials.local.json")
    local = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not isinstance(local, dict):
        raise ValueError("credentials.local.json must contain a JSON object")
    value = os.environ.get(name) or local.get(name)
    if not value and fallback:
        value = os.environ.get(fallback) or local.get(fallback)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"Set {name} in the environment or credentials.local.json")
    return value
