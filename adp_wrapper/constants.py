from datetime import timedelta

# Date formats
ADP_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

# app name for keyring
APP_NAME = "adp_butler"

USERNAME_PROMPT = "Username : "
PASSWORD_PROMPT = "Password : "
GOODBYE_MESSAGE = "\nGoodbye."

# daily total required work time
DAILY_WORK_TIME = timedelta(hours=7, minutes=24)

# URLs for ADP services
URL_LOGIN = "https://mon.adp.com/ipclogin/1/loginform.fcc"
URL_PUNCH = "https://mon.adp.com/v1_0/O/A/timeEntryDetails"
URL_PUNCH_SUBMIT = "https://mon.adp.com/v1_0/O/A/timeEntry"
URL_REQUEST_WFH_SUBMIT = "https://mon.adp.com/events/time/v1/time-off-request.submit"
URL_TIMEOFF_REQUESTS = (
    "https://mon.adp.com/time/v3/workers/" + "__REDACTED__" + "/time-off-requests"
)
