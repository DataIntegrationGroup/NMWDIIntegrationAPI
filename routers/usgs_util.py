# ===============================================================================
# Copyright 2023 Jake Ross
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
import pprint

import httpx


def get_latest_gw_data(sites):
    nwis_gwlevels = get_nwis_gwlevels(sites)
    nwis_iv_gwlevels = get_nwis_iv_gwlevels(sites)
    nwis_dv_gwlevels = get_nwis_dv_gwlevels(sites)

    nwis_gwlevels.extend(nwis_iv_gwlevels)
    nwis_gwlevels.extend(nwis_dv_gwlevels)
    return nwis_gwlevels


def get_nwis_gwlevels(sites):
    allrecords = []
    baseurl = "https://waterservices.usgs.gov/nwis/gwlevels/?format=rdb&siteStatus=all"
    for sitesi in _divide_chunks(sites, 100):
        url = f'{baseurl}&sites={",".join(sitesi)}'
        with httpx.Client(headers={"Accept-Encoding": "gzip, compress"}) as client:
            r = client.get(url)
            if r.status_code == 200:
                records = make_records(r.text, url)
                allrecords.extend(records)
    return allrecords


def get_nwis_iv_gwlevels(sites):
    baseurl = "https://waterservices.usgs.gov/nwis/iv/?format=json&parameterCd=72019"
    return _get_nwis_gwlevels(sites, baseurl)


def get_nwis_dv_gwlevels(sites):
    baseurl = "https://waterservices.usgs.gov/nwis/dv/?format=json&parameterCd=72019"
    return _get_nwis_gwlevels(sites, baseurl)


def _divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def _get_nwis_gwlevels(sites, baseurl):
    allrecords = []
    for sitesi in _divide_chunks(sites, 100):
        url = f'{baseurl}&sites={",".join(sitesi)}'
        with httpx.Client(headers={"Accept-Encoding": "gzip, compress"}) as client:
            r = client.get(url)
            if r.status_code == 200:
                rj = r.json()
                records = _make_json_records(rj, url, "iv")
                allrecords.extend(records)
    return allrecords


def _make_json_records(js, url, tag):
    records = []
    for site in js["value"]["timeSeries"]:
        site_no = site["sourceInfo"]["siteCode"][0]["value"]
        for value in site["values"][0]["value"]:
            record = {
                "site_no": site_no,
                "date_time": value["dateTime"],
                "value": value["value"],
                "url": url,
                "tag": tag,
            }
            records.append(record)
    return records


def get_site_metadata(
    siteid=None, parameterCode=None, siteType="GW", stateCd="NM"
):
    """
    get site metadata from USGS
    :param location:
    :return:
    """
    url = f"https://waterservices.usgs.gov/nwis/site/?format=rdb&siteStatus=all&siteOutput=expanded"
    if siteid is not None:
        url = f"{url}&sites={siteid}"
    else:
        url = f"{url}&siteType={siteType}&stateCd={stateCd}"

    if parameterCode is not None:
        url = f"{url}&parameterCd={parameterCode}"

    with httpx.Client() as client:
        r = client.get(url)
        if r.status_code == 200:
            records = make_records(r.text, url)
            return records[0] if siteid else records
        else:
            return r.status_code

    # resp = requests.get(url)
    # if resp.status_code == 200:
    #     return_dict = make_site_record(resp.text)
    #     return_dict["url"] = url
    #     return return_dict
    # else:
    #     return resp.status_code


def make_records(txt, url, tag=None):
    header = ""
    records = []
    for line in txt.split("\n"):
        if line.startswith("#"):
            continue

        if line.startswith("agency_cd"):
            header = [h.strip() for h in line.split("\t")]
            continue

        if line.startswith("5s"):
            continue

        record = dict(zip(header, [l.strip() for l in line.split("\t")]))

        if record["agency_cd"] == "":
            continue
        record["url"] = url
        if tag:
            record["tag"] = tag
        records.append(record)
    return records


# ============= EOF =============================================
