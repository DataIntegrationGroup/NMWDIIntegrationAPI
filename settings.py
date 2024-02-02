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
import os


class Settings:
    """
    Versioning rules.
    X.Y.Z
    X - major version. incompatible API changes
    Y - minor version. backward compatible API changes. new features
    Z - patch version. backward compatible bug fixes. cosmetic changes
    """

    VERSION = "0.4.0"
    ALLOWED_HOSTS: list = ["*"]

    def __init__(self):
        self.IS_LOCAL = os.getenv("IS_LOCAL", True)
        self.SECRET_KEY = os.getenv("SECRET_KEY")


settings = Settings()

# ============= EOF =============================================
