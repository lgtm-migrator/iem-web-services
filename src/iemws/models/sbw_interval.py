"""Model of vtec/sbw_interval service."""

# third party imports
from pydantic import BaseModel, Field


class SBWIntervalModel(BaseModel):
    """Data Schema."""

    utc_issue: str = Field(..., title="Issuance UTC timestamp")
    utc_expire: str = Field(..., title="Expiration UTC timestamp")
    utc_polygon_begin: str = Field(..., title="Polygon Begin UTC timestamp")
    utc_polygon_end: str = Field(..., title="Polygon End UTC timestamp")
    ph_sig: str = Field(..., title="Phenomena.Significance")
    wfo: str = Field(..., title="WFO")
    eventid: int = Field(..., title="Event ID")
    phenomena: str = Field(..., title="Phenomena")
    significance: str = Field(..., title="Significance")
    nws_color: str = Field(..., title="NWS Color")
    event_label: str = Field(..., title="Event Label")
    status: str = Field(..., title="Status")
