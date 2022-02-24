"""List NWS Text Products Metadata.

This service returns metadata and hrefs for IEM stored NWS Text Products. The
`product_id` can be used to call `/api/1/nwstext/{product_id}` to retrieve the
actual text.

The provided `cccc` (WMO Source Code) can be provided as a three character
identifier.  In that case, a `K` is prepended to rectify it.
"""
import datetime

# Third Party
from pandas.io.sql import read_sql
from fastapi import Query, APIRouter
from pyiem.util import utc, get_sqlalchemy_conn

# Local
from ....models import SupportedFormatsNoGeoJSON
from ....models.afos.list import AFOSListSchema
from ....util import deliver_df

ISO = "YYYY-MM-DDThh24:MI:SSZ"
router = APIRouter()


def handler(cccc, date):
    """Handle the request, return df."""
    sts = utc(date.year, date.month, date.day)
    ets = sts + datetime.timedelta(days=1)
    with get_sqlalchemy_conn("afos") as conn:
        df = read_sql(
            """
            select entered at time zone 'UTC' as entered, pil,
            to_char(entered at time zone 'UTC', 'YYYYmmddHH24MI') || '-' ||
            source || '-' || wmo || '-' || trim(pil) ||
            (case when bbb is not null then '-' || bbb else '' end)
            as product_id
            from products where source = %s and entered >= %s
            and entered < %s ORDER by entered ASC
            """,
            conn,
            params=(cccc, sts, ets),
            index_col=None,
        )
    return df


@router.get(
    "/nws/afos/list.{fmt}",
    description=__doc__,
    response_model=AFOSListSchema,
    tags=[
        "nws",
    ],
)
def service(
    fmt: SupportedFormatsNoGeoJSON,
    cccc: str = Query(..., min_length=3, max_length=4),
    date: datetime.date = Query(None),
):
    """Replaced above."""
    if date is None:
        date = utc()
    if len(cccc) == 3:
        cccc = f"K{cccc}"
    df = handler(cccc.upper(), date)
    return deliver_df(df, fmt)


service.__doc__ = __doc__
