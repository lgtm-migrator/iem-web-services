"""
Return to [IEM API Homepage](https://mesonet.agron.iastate.edu/api/).

This answers `/api/1/` versioned requests against the IEM.  This service is
driven by the awesome [FastAPI](https://fastapi.tiangolo.com/) Python library.

"""

from fastapi import FastAPI
from .services import (
    currents,
    cow,
    drydown,
    ffg_bypoint,
    meteobridge,
    nwstext,
    shef_currents,
    usdm_bypoint,
    servertime,
    spc_watch_outline,
)

app = FastAPI(openapi_prefix="/api/1", description=__doc__, title="IEM API v1")

# /servertime
servertime.factory(app)

# /ffg_bypoint.geojson
ffg_bypoint.factory(app)

# /usdm_bypoint.json
usdm_bypoint.factory(app)

# /shef_currents.{fmt}
shef_currents.factory(app)

# /nwstext/{product_id}
nwstext.factory(app)

# /meteobridge.json
meteobridge.factory(app)

# /drydown.json
drydown.factory(app)

# /cow.json
cow.factory(app)

# /currents.{fmt}
currents.factory(app)

# /spc_watch_outline.geojson
spc_watch_outline.factory(app)
