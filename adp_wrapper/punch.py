import json
import logging
from datetime import datetime

from requests import Session

from adp_wrapper.auth import SessionTimeoutException
from adp_wrapper.constants import URL_PUNCH, URL_PUNCH_SUBMIT, URL_REFERER, get_setting

log = logging.getLogger(__name__)


class PunchException(Exception):
    def __init__(self, timestamp: datetime) -> None:
        self.timestamp = timestamp
        self.message = f"an error occured while punching at {timestamp.isoformat()}"
        log.error("PunchException : " + self.message)
        super().__init__(self.message)


def get_punch_times(s: Session) -> list[datetime]:
    """get the punch times from adp

    Args:
        s (requests.Session): browser session

    Returns:
        list[datetime]: list of punch times
    """
    params = (("entryNotes", "yes"),)  # does not seem to change anything
    response = s.get(URL_PUNCH, params=params)

    if "application/json" in response.headers.get("content-type"):
        response_json = response.json()
    else:
        raise SessionTimeoutException()

    entries: dict = response_json["timeEntryDetails"]["entrySummary"][0]
    if "entries" in entries:
        pointages: list = entries["entries"][0]["entryDetail"][0]["clockSummary"][
            "clockEntries"
        ]
    else:
        # value is not formatted correctly, happens when there is no punch times
        pointages = []

    result = []
    for p in pointages:
        date = datetime.strptime(p["entryDateTime"], "%Y-%m-%dT%H:%M:%S%z")
        result.append(date)

    log.info(f"retrieved {len(result)} punch times")
    return result


def punch(s: Session, timestamp: datetime) -> bool:
    """clocks in or out to adp

    Args:
        s (requests.Session): browser session
        timestamp (datetime): time at which to punch

    Returns:
        bool: response was successful

    Raises:
        PunchException
    """
    user_id = str(get_setting("adp_username"))

    time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    data = {
        "timeEntry": {
            "metadeviceDateTime": time + "+01:00",
            "positionID": {
                "id": user_id,
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
        "Referer": URL_REFERER,
    }

    response_punch = s.post(URL_PUNCH_SUBMIT, data=data_str, headers=headers)

    if response_punch.ok:
        log.info(f"punch successful at {timestamp.isoformat()}")
        return True
    else:
        raise PunchException(timestamp)
