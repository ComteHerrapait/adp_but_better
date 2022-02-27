import datetime
import json

import requests

data = {
    "user": "__REDACTED__",
    "password": "ADPlyx42?",
    "target": "https://mon.adp.com/redbox/",
}
# LOGIN
with requests.Session() as s:

    r_login = s.post("https://mon.adp.com/ipclogin/1/loginform.fcc", data=data)

    print("STATUS : ", r_login.status_code)
    print(str(s.cookies.get("EMEASMSESSION"))[:20], "...")

    r_get_data = s.get("https://mon.adp.com/v1_0/O/A/timeEntryDetails")
    print("STATUS : ", r_login.status_code)
    print(str(s.cookies.get("EMEASMSESSION"))[:20], "...")

    try:
        response_json = r_get_data.json()
    except json.decoder.JSONDecodeError:
        exit("Error : Can't decode json. Most probably the session has expired.")

    entries = response_json["timeEntryDetails"]["entrySummary"][0]["entries"]
    pointages = entries[0]["entryDetail"][0]["clockSummary"]["clockEntries"]

    for p in pointages:
        date = datetime.datetime.strptime(p["entryDateTime"], "%Y-%m-%dT%H:%M:%S%z")
        code = p["actionCode"]
        description = p["description"]
        date_string = date.strftime("%H:%M:%S")
        print(f"{code} : {date_string}")
