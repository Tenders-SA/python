from __future__ import annotations

import re
from typing import Any


def _camel_to_snake(name: str) -> str:
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def convert_keys(d: Any) -> Any:
    if isinstance(d, dict):
        return {_camel_to_snake(k): convert_keys(v) for k, v in d.items()}
    if isinstance(d, list):
        return [convert_keys(v) for v in d]
    return d
