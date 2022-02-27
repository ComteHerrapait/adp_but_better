import json
from datetime import datetime

import requests

from constants import ADP_DATE_FORMAT, URL_REQUEST_WFH_SUBMIT, URL_TIMEOFF_REQUESTS


def submit_working_from_home_request(session: requests.Session, day: datetime) -> bool:
    response = session.post(
        URL_REQUEST_WFH_SUBMIT,
        data=data_wfh_request(employee_id="__REDACTED__", date=day),
    )
    return response.status_code == 200


# flake8: noqa: C901
def get_wfh_requests(session: requests.Session):
    # TODO : study and use the filter (I don't know how it works, it ignores what I ask for)
    # TODO : remove noqa tag (ignore errors for flake9, because it's still a work in progress)
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


def data_wfh_request(employee_id: str, date: datetime, comment: str = "") -> str:
    date_str = date.strftime("%Y-%m-%dT00:00:00+01:00")
    data_new = {
        "events": [
            {
                "data": {
                    "eventContext": {"associateOID": employee_id},
                    "transform": {
                        "timeOffRequest": {
                            "timeOffEntries": [
                                {
                                    "timeOffPolicyCode": {"codeValue": "TTRAV2"},
                                    "durationTypeCode": {"codeValue": "dayPeriodEntry"},
                                    "dateTimePeriod": {
                                        "startDateTime": date_str,
                                        "endDateTime": date_str,
                                    },
                                    "dayPeriodStartCode": {
                                        "codeValue": "M",
                                        "shortName": "Matin",
                                    },
                                    "dayPeriodEndCode": {
                                        "codeValue": "A",
                                        "shortName": "Apr\xE8s-midi",
                                    },
                                    "payCode": {
                                        "codeValue": "TTRAV2",
                                        "shortName": "T\xE9l\xE9travail s\xE9dentaire",
                                    },
                                }
                            ],
                            "comment": {"textValue": comment},
                        }
                    },
                }
            }
        ]
    }
    return json.dumps(data_new, separators=(",", ":"))


if __name__ == "__main__":
    from auth import adp_login

    s = requests.Session()
    adp_login(s, "__REDACTED__", "__REDACTED__")
    get_wfh_requests(s)
