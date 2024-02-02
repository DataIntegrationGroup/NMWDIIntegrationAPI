# ===============================================================================
# Copyright 2024 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from routers import usgs_util
from schemas.waterlevel import NMWDIWaterLevel

router = APIRouter(
    prefix="/nwis",
    tags=["nwis"],
)


@router.get(
    "/gw/locations",
)
@cache(expire=3600)
async def get_locations(limit: int = None):
    locations = await usgs_util.get_site_metadata(parameterCode="72019")

    def make_feature(loc):
        loc["name"] = loc["site_no"]
        loc["well_depth"] = {"value": loc["well_depth_va"], "units": "ft"}
        loc["hole_depth"] = {"value": loc["hole_depth_va"], "units": "ft"}

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    loc["dec_long_va"],
                    loc["dec_lat_va"],
                    float(loc["alt_va"]) * 0.3048,
                ],
            },
            "properties": loc,
        }
        return feature

    locations = [
        l
        for l in locations
        if "dec_long_va" in l and "dec_lat_va" in l and "alt_va" in l
    ]
    if limit:
        locations = locations[:limit]
    return {
        "type": "FeatureCollection",
        "features": [make_feature(loc) for loc in locations],
    }


def transform_latest(record):
    try:
        record["depth_to_water_ftbgs"] = float(record["lev_va"])
    except (ValueError, TypeError, KeyError):
        return

    record["date_measured"] = record["lev_dt"]
    record["site_id"] = record["site_no"]
    return record


@router.post("/gw/waterlevels/latest", response_model=List[NMWDIWaterLevel])
async def get_latest_gw_data(sites: List[str]):
    records = usgs_util.get_latest_gw_data(sites)
    records = [transform_latest(record) for record in records]
    return [r for r in records if r is not None]


# ============= EOF =============================================
