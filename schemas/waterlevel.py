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
from datetime import date, time, datetime
from typing import Union

from pydantic import BaseModel


class NMWDIWaterLevel(BaseModel):
    site_id: str
    depth_to_water_ftbgs: float
    date_measured: Union[date, datetime]
    time_measured: Union[time, None] = None


# ============= EOF =============================================
