import dataclasses
import json
import logging
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any

import requests
from requests import Session

from adp_wrapper.auth import SessionTimeoutException
from adp_wrapper.constants import (
    API_VERSION,
    DATE_FORMAT,
    DATETIME_FORMAT,
    URL_REFERER,
    URL_REQUEST_WFH_SUBMIT,
    URL_TIMEOFF_META,
    URL_TIMEOFF_REQUESTS,
    get_setting,
)

log = logging.getLogger(__name__)


class TimeOffRequestException(Exception):
    def __init__(self) -> None:
        self.message = "an error occured while requesting timeoff"
        log.error("TimeOffRequestException : " + self.message)
        super().__init__(self.message)


class PeriodCode(Enum):
    morning = {"codeValue": "M", "shortName": "Matin"}
    afternoon = {"codeValue": "A", "shortName": "Apr\xE8s-midi"}

    def to_dict(self) -> dict:
        return {
            "codeValue": self.value["codeValue"],
            "shortName": self.value["shortName"],
        }


@dataclass
class TimeOffEvent:
    code: str = ""
    name: str = ""
    comment: str = ""
    date_start: date = date.today()
    date_end: date = date.today()
    period_start: PeriodCode = PeriodCode.morning
    period_end: PeriodCode = PeriodCode.afternoon

    def to_dict(self) -> dict:
        return {
            "timeOffPolicyCode": {"codeValue": self.code},
            "durationTypeCode": {"codeValue": "dayPeriodEntry"},
            "dateTimePeriod": {
                "startDateTime": self.date_start.strftime("%Y-%m-%dT00:00:00+01:00"),
                "endDateTime": self.date_end.strftime("%Y-%m-%dT00:00:00+01:00"),
            },
            "dayPeriodStartCode": self.period_start.to_dict(),
            "dayPeriodEndCode": self.period_end.to_dict(),
            "payCode": {
                "codeValue": self.code,
                "shortName": self.name,
            },
        }


@dataclass
class TimeOffRequest:
    id: str = ""
    creation_date: datetime = datetime.min
    status: str = ""  # TODO : enum
    status_date: date = date.min
    requestor: str = ""
    event: TimeOffEvent = TimeOffEvent()


class EnhancedJSONEncoder(json.JSONEncoder):
    """Enhances the JSONEncoder class to handle dataclasses, datetime and Enum."""

    def default(self, o: Any) -> (dict[str, Any] | str | Any):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


def send_timeoff_request(
    session: Session,
    events: list[TimeOffEvent],
    comment: str = "",
) -> bool:

    request_body = build_body_timeoff_request(events, comment)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://mon.adp.com",
        "Referer": URL_REFERER,
    }

    data_str = json.dumps(request_body, separators=(",", ":"))
    response = session.post(
        URL_REQUEST_WFH_SUBMIT,
        data=data_str,
        headers=headers,
    )
    if response.ok:
        log.info("successfully sent timeoff request")
        return True
    else:
        raise TimeOffRequestException()


def build_body_timeoff_request(events: list[TimeOffEvent], comment: str = "") -> dict:
    return {
        "events": [
            {
                "data": {
                    "eventContext": {"associateOID": get_setting("adp_username")},
                    "transform": {
                        "timeOffRequest": {
                            "timeOffEntries": [event.to_dict() for event in events],
                            "comment": {"textValue": comment},
                        }
                    },
                }
            }
        ]
    }


def get_pay_codes(session: Session) -> list[TimeOffEvent]:
    raw_data = send_time_off_meta_request(session)
    data: list[TimeOffEvent] = []

    if not raw_data:
        return data
    else:
        raw_data = raw_data["meta"]

    pay_codes = raw_data["/data/transforms"][0][
        "/timeOffRequest/timeOffEntries/payCode"
    ]["dependencies"]["codeList"]["allOf"]
    for code in pay_codes:
        raw = {
            "code": code["value"][0]["codeValue"],
            "name": code["value"][0]["shortName"],
        }
        data.append(TimeOffEvent(**raw))
    return data


def send_time_off_meta_request(session: Session) -> Any:

    headers = {"Referer": URL_REFERER}

    response = session.get(URL_TIMEOFF_META, headers=headers)

    return response.json()


def get_timeoff_requests(session: requests.Session) -> list:

    filter_start = datetime.strftime(datetime.min, DATE_FORMAT)
    filter_end = datetime.strftime(datetime.max, DATE_FORMAT)
    params = (
        (
            "$filter",
            f"datePeriod/startDate ge '{filter_start}'"
            f" and datePeriod/endDate le '{filter_end}'",
        ),
    )

    headers = {"Referer": URL_REFERER}
    url = URL_TIMEOFF_REQUESTS.replace("<USER_ID>", get_setting("adp_username"))
    response = session.get(url, params=params, headers=headers)

    if "application/json" not in response.headers.get("content-type", ""):
        raise SessionTimeoutException()
    timeoff_requests = response.json()["timeOffRequests"]

    requests = []
    for r in timeoff_requests:
        start = datetime.strptime(
            r["timeOffEntries"][0]["dateTimePeriod"]["startDateTime"],
            DATETIME_FORMAT,
        )
        end = datetime.strptime(
            r["timeOffEntries"][0]["dateTimePeriod"]["endDateTime"], DATETIME_FORMAT
        )
        event = TimeOffEvent(
            code=r["timeOffEntries"][0]["payCode"]["codeValue"],
            name=r["timeOffEntries"][0]["payCode"]["shortName"],
            date_start=start,
            date_end=end,
        )

        request = TimeOffRequest(
            id=r["timeOffRequestID"],
            creation_date=datetime.strptime(r["requestDateTime"], DATETIME_FORMAT),
            status=r["requestStatusCode"]["codeValue"],
            status_date=datetime.strptime(
                r["requestStatusCode"]["effectiveDate"], DATE_FORMAT
            ).date(),
            requestor=r["requestorName"]["formattedName"],
            event=event,
        )
        requests.append(request)
    requests.sort(key=lambda x: x.creation_date)
    log.info(f"retrieved {len(requests)} timeoff requests")
    return requests
