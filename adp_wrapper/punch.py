import json
from datetime import datetime

import requests

from adp_wrapper.constants import URL_PUNCH, URL_PUNCH_SUBMIT


def get_punch_times(s: requests.Session) -> list[datetime]:
    params = (("entryNotes", "yes"),)  # does not seem to change anything
    response = s.get(URL_PUNCH, params=params)

    try:
        response_json = response.json()
    except json.decoder.JSONDecodeError:
        exit("Error : Can't decode json. Most probably the session has expired.")

    try:
        entries = response_json["timeEntryDetails"]["entrySummary"][0]["entries"]
        pointages = entries[0]["entryDetail"][0]["clockSummary"]["clockEntries"]
    except KeyError:
        return []

    result = []
    for p in pointages:
        date = datetime.strptime(p["entryDateTime"], "%Y-%m-%dT%H:%M:%S%z")
        result.append(date)
    return result


def punch(s: requests.Session, timestamp: datetime) -> bool:

    time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    data = {
        "timeEntry": {
            "metadeviceDateTime": time + "+01:00",
            "positionID": {
                "id": "__REDACTED__",
                "schemeName": "PFID",
                "schemeAgencyName": "ADP Registry",
            },
            "clockEntry": {"entryDateTime": time + "+01:00", "actionCode": "punch"},
        }
    }
    data_str = json.dumps(data, separators=(",", ":"))
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://mon.adp.com",
        "Referer": "https://mon.adp.com/redbox/3.10.1.2/",
    }

    response_punch = s.post(URL_PUNCH_SUBMIT, data=data_str, headers=headers)
    return response_punch.status_code == 201
