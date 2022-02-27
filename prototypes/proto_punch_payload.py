import datetime
import json

timestamp = datetime.datetime.now()

time = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
data_correct = (
    '{"timeEntry":{"metadeviceDateTime":"'
    + time
    + '+01:00","positionID":{"id":"__REDACTED__","schemeName":"PFID","schemeAgencyName":"ADP Registry"},"clockEntry":{"entryDateTime":"'
    + time
    + '+01:00","actionCode":"punch"}}}'
)

data_test = {
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
data_test = json.dumps(data_test, separators=(",", ":"))
data_match = data_correct == data_test
print(data_match)
if data_match:
    print("The two payload match !")
else:
    print("The two payload don't match !")
    print(data_correct)
    print(data_test)
