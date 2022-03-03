import json
from datetime import timedelta
from pathlib import Path
from typing import Any

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
URL_SEARCH_USERS = "https://mon.adp.com/core/v1/search"
URL_DETAIL_USER = "https://mon.adp.com/redboxapi/core/profile/v1/associates/"
URL_BALANCES = "https://mon.adp.com/time/v3/workers/<USER_ID>/time-off-balances"
URL_TIMEOFF_REQUESTS = "https://mon.adp.com/time/v3/workers/<USER_ID>/time-off-requests"
URL_REFERER = "https://mon.adp.com/redbox/3.10.1.2"


SETTINGS_FILE = Path("config.json")
DEFAULT_SETTINGS = {
    "adp_username": "",
    "skip_password_prompt": False,
}


def get_setting(key: str) -> Any:
    """get a setting from the config file

    Args:
        key (str): name of the setting to get

    Returns:
        Any: value of the setting
    """
    if SETTINGS_FILE.exists():
        with open("config.json", "r") as f:
            value = json.load(f).get(key, None)
    else:
        value = None

    if value is None:
        set_setting(key, DEFAULT_SETTINGS[key])
        value = DEFAULT_SETTINGS[key]

    return value


def set_setting(key: str, value: Any) -> None:
    """set the value of a setting in the config file

    Args:
        key (str): name of the setting to set
        value (Any): value of the setting
    """
    if SETTINGS_FILE.exists():
        with SETTINGS_FILE.open("r") as f:
            settings = json.load(f)
    else:
        settings = DEFAULT_SETTINGS

    settings[key] = value

    with SETTINGS_FILE.open("w") as f:
        json.dump(settings, f, indent=4)
