"""IEM-Only API used to feed in Meteobridge Data.

Unuseful for you all :)
"""
# pylint: disable=unused-argument
import datetime

import pytz
from fastapi import Query, HTTPException, APIRouter
from pyiem.util import get_properties, utc, get_dbconn
from pyiem.observation import Observation

PROPS = {}
router = APIRouter()


def handler(
    key, time, tmpf, max_tmpf, min_tmpf, dwpf, relh, sknt, pday, alti, drct
):
    """Handle the request, return dict"""
    # sys.stderr.write(repr(fields))
    if not PROPS:
        PROPS.update(get_properties())
    lookup = {}
    for sid in ["OT0013", "OT0014", "OT0015", "OT0016"]:
        lookup[PROPS.get("meteobridge.key." + sid)] = sid
    if key not in lookup:
        raise HTTPException(status_code=404, detail="BAD_KEY")
    sid = lookup[key]
    if len(time) == 14:
        _t = time
        now = utc(
            int(_t[:4]),
            int(_t[4:6]),
            int(_t[6:8]),
            int(_t[8:10]),
            int(_t[10:12]),
            int(_t[12:14]),
        )
    else:
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)
    ob = Observation(sid, "OT", now)
    for fname in [
        "tmpf",
        "max_tmpf",
        "min_tmpf",
        "dwpf",
        "relh",
        "sknt",
        "pday",
        "alti",
        "drct",
    ]:
        if vars()[fname] == "M":
            continue
        ob.data[fname] = float(vars()[fname])
    pgconn = get_dbconn("iem")
    cursor = pgconn.cursor()
    ob.save(cursor)
    cursor.close()
    pgconn.commit()
    return "OK"


@router.get(
    "/meteobridge.json",
    description=__doc__,
    tags=[
        "debug",
    ],
)
def meteobridge_service(
    key: str = Query(...),
    time: str = Query(...),
    tmpf: str = Query(...),
    max_tmpf: str = Query(...),
    min_tmpf: str = Query(...),
    dwpf: str = Query(...),
    relh: str = Query(...),
    sknt: str = Query(...),
    pday: str = Query(...),
    alti: str = Query(...),
    drct: str = Query(...),
):
    """Replaced above with __doc__."""
    return handler(
        key,
        time,
        tmpf,
        max_tmpf,
        min_tmpf,
        dwpf,
        relh,
        sknt,
        pday,
        alti,
        drct,
    )


meteobridge_service.__doc__ = __doc__
