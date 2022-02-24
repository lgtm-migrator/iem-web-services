"""Models for iemre API."""
# pylint: disable=no-name-in-module,too-few-public-methods
from typing import List

from pydantic import BaseModel, Field


class AFOSListItem(BaseModel):
    """Data Schema."""

    entered: str = Field(..., title="WMO Text Product Issuance Time (UTC)")
    pil: str = Field(..., title="Three to Six Letter Product ID")
    product: str = Field(..., title="IEM Text Product ID.")


class AFOSListSchema(BaseModel):
    """The schema used by this service."""

    data: List[AFOSListItem]
