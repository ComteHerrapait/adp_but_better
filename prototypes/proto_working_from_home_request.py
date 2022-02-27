import json
from datetime import datetime

import requests

cookies = {
    "mlOqCpOrig": "rd1o00000000000000000000ffff0b81c0b4o1073",
    "9NsIAD8oR9": "AA8e6tB-AQAAS84IavMOwZ4lVfykRESYltARHIME8qZldoOr0urKqrizcBfv|1|1|881218f557f038efeacc0a5a11caa69b4014827f",
    "FRANCE-PORTAL": "rd1o00000000000000000000ffff0b81c303o8080",
    "ADPEHCRELEASE": "----S-6-----------------------a---1-----------------------------4------12----2-------------------------------------------1",
    "disconnecturl": "https://hr-services.fr.adp.com/portal-main/postconnect.jsp",
    "EMEASMSESSION": "hafsrL5HkH21YlTvC/8Wy3eNZSd2XQp4kWigekRCYF5h4gXUaM7tg+m0JaapAMHBmq+30YdIb2UCK2lcxcNJ79Qspvbt550nRtaDYB9b5dhvb2qcsSuwSrBIH9wD5HHFj9RH+EAiCowckzVtrWKjyVPlkKNegPPOOvVaN5a/Mdts1o0TL/YAlBbq2sSDM1rEm0KUic9dWeyJMHWG5AR2rPVJLbYTI6MA0XRWv4VzAHI6AzfthrnQzCBwCITSdhEVGvpMPYanczSSAIXDF7xgvNSp5LLUSlGWM6xa+bdDONdKePls0gg4iebdk27sqxxeNoXgMuSPihjJVKxKVVh2wbz2y5T+feDgPsrYIivM58OQpBAgyYatPVVJv7NA36ugG3AXpQ9OZt4xdh5I1wmiJVs+gh18k+mU4ksYLJIfJ5bD4O4c4SNFZKAsYUK4tdl/kUGmaj6Shk2OM+3+p2RMgQY9Y5mtFaZcG/9Jck29X2QI2vzBHmWOPwKtX8mGqVhk1ZyNRiHLsVYx4wV3Tr7pJW3RnpWtNlhguObVRlw5qPQS7Oxg8Xs+DUpioRpOK/nQUydR4+BRhsEroXvU0vzEJb4uaqAwRw3UllrWP1VEGYokbxWth7TG8sWwzw+G9+q+Ym4r8TIqw25z3P+U8jR+9Ddcy9AvJVqFHKCr9qDfNPOsv9QPkuxxjgCGVA/8gPnR7EmjVB77fXYw8XJ/1HW/ylgrs0ert5snTKsdc2RS9uZhIaXLA2Uz2nKM3dW+JeuB/n+b+j3JizSbM0yEnRVBJiBjmZpMztVTw52OW20etc+vBE6WL2yB6RJOsfHs9/7Fhg24R9TPIG1rqazUk+FyBukb5R3nFaCTG1cjD3H/cgjN53m41FHJkZE+TUMxKCtq7MV2M8t/i3rckyQ2klo0LevCUrH7VCdR2+0uvDJJ939VriREMMmDyNLR1iYLfYnX+PAkTdArAEALmMy+nG7W5Nn8Uyat+UBsktDWgh7u+SWDcwyclamG5ZQPWHIuVqzOT239aUX55YEDCBYlF+O++Xpmw3Kq70JcoN2K2/BV6cll4nvd0viZWYeMGMpCIujVGvb53K8Ip9nhot1+CP8GDx52Fpao0NJPa5avHXPt9pluVY9acKz+ib7DuiUzzWjm",
}

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "Accept-Language": "fr-FR",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "rolecode": "employee",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "consumerappoid": "RDBX:3.10",
    "sec-ch-ua-platform": '"macOS"',
    "Origin": "https://mon.adp.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mon.adp.com/redbox/3.10.1.2/",
}

# data = '{"events":[{"data":{"eventContext":{"associateOID":"__REDACTED__"},"transform":{"timeOffRequest":{"timeOffEntries":[{"timeOffPolicyCode":{"codeValue":"TTRAV2"},"durationTypeCode":{"codeValue":"dayPeriodEntry"},"dateTimePeriod":{"startDateTime":"2022-02-07T00:00:00+01:00","endDateTime":"2022-02-07T00:00:00+01:00"},"dayPeriodStartCode":{"codeValue":"M","shortName":"Matin"},"dayPeriodEndCode":{"codeValue":"A","shortName":"Apr\xE8s-midi"},"payCode":{"codeValue":"TTRAV2","shortName":"T\xE9l\xE9travail s\xE9dentaire"}}],"comment":{"textValue":"t\xE9l\xE9travail"}}}}}]}'

EMPLOYEE_ID = "__REDACTED__"
DATE = datetime.now().replace(day=10)
STR_DATE = DATE.strftime("%Y-%m-%dT00:00:00+01:00")
data_new = {
    "events": [
        {
            "data": {
                "eventContext": {"associateOID": EMPLOYEE_ID},
                "transform": {
                    "timeOffRequest": {
                        "timeOffEntries": [
                            {
                                "timeOffPolicyCode": {"codeValue": "TTRAV2"},
                                "durationTypeCode": {"codeValue": "dayPeriodEntry"},
                                "dateTimePeriod": {
                                    "startDateTime": STR_DATE,
                                    "endDateTime": STR_DATE,
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
                        "comment": {"textValue": "t\xE9l\xE9travail"},
                    }
                },
            }
        }
    ]
}

data_new_str = json.dumps(data_new, separators=(",", ":"))
print(data_new_str)

response = requests.post(
    "https://mon.adp.com/events/time/v1/time-off-request.submit",
    headers=headers,
    cookies=cookies,
    data=data_new_str,
)

print(response.status_code)
print(response.text)
