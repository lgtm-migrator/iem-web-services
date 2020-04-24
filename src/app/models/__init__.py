"""Place holder."""
from enum import Enum


class SupportedFormats(str, Enum):
    """Formats supported by service."""

    json = "json"
    geojson = "geojson"
    txt = "txt"
