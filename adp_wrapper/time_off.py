import dataclasses
import json
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any

import requests
from requests import Session

from adp_wrapper.constants import (
    ADP_DATE_FORMAT,
    URL_REFERER,
    URL_REQUEST_WFH_SUBMIT,
    URL_TIMEOFF_META,
    URL_TIMEOFF_REQUESTS,
    get_setting,
)


class PeriodCode(Enum):
    morning = {"codeValue": "M", "shortName": "Matin"}
    afternoon = {"codeValue": "A", "shortName": "Apr\xE8s-midi"}

    def to_dict(self):
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

    def to_dict(self):
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


class EnhancedJSONEncoder(json.JSONEncoder):
    """Enhances the JSONEncoder class to handle dataclasses, datetime and Enum."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


def print_json(obj: Any, **kwargs) -> None:
    """Prints a JSON representation of the given object.

    Args:
        obj (Any): object to print
        **kwargs: additional arguments passed to json.dumps
    """
    print(json.dumps(obj, cls=EnhancedJSONEncoder, **kwargs))


def send_timeoff_request(
    session: Session,
    events: list[TimeOffEvent],
    comment: str = "",
):

    request_body = build_body_timeoff_request(events, comment)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://mon.adp.com",
        "Referer": "https://mon.adp.com/redbox/3.10.1.2/",
    }

    data_str = json.dumps(request_body, separators=(",", ":"))
    response = session.post(
        URL_REQUEST_WFH_SUBMIT,
        data=data_str,
        headers=headers,
    )
    return response.ok


def build_body_timeoff_request(events: list[TimeOffEvent], comment: str = ""):
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
    data = []

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


def send_time_off_meta_request(session: Session):

    headers = {"Referer": URL_REFERER}

    response = session.get(URL_TIMEOFF_META, headers=headers)

    return response.json()


# flake8: noqa: C901
def get_wfh_requests(session: requests.Session):
    # TODO : study and use the filter (I don't know how it works, it ignores what I ask for)
    params = (
        (
            "$filter",
            "datePeriod/startDate ge '1970-01-05' and datePeriod/endDate le '2999-01-05'",
            # "datePeriod/startDate ge '2020-02-06' and datePeriod/endDate le '2023-02-06' ",
            # "datePeriod/startDate ge '2020-02-06' and datePeriod/endDate le '2023-02-06' and requestStatusCode/codeValue eq 'submitted' and requestStatusCode/codeValue eq 'pending' and requestStatusCode/codeValue eq 'cancelsubmitted' and requestStatusCode/codeValue eq 'inprogress'",
        ),
    )

    response = session.get(
        URL_TIMEOFF_REQUESTS,
        params=params,
    )
    print(response.json())
    wfh_requests = response.json()["timeOffRequests"]
    summary = []
    for r in wfh_requests:
        start = datetime.strptime(
            r["timeOffEntries"][0]["dateTimePeriod"]["startDateTime"],
            ADP_DATE_FORMAT,
        )
        end = datetime.strptime(
            r["timeOffEntries"][0]["dateTimePeriod"]["endDateTime"], ADP_DATE_FORMAT
        )
        summary.append(
            {
                "id": r["timeOffRequestID"],
                "status": r["requestStatusCode"]["codeValue"],
                "start": datetime.strftime(start, "%Y-%m-%d"),
                "end": datetime.strftime(end, "%Y-%m-%d"),
                "type": r["timeOffEntries"][0]["payCode"]["codeValue"],
            }
        )
    summary.sort(key=lambda x: x["start"])
    print(json.dumps(summary, indent=4))
