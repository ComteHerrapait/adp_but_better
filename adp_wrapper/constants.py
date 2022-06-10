import json
import logging
from datetime import timedelta
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


# Date formats
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_FORMAT = "%Y-%m-%d"

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
URL_DETAIL_USER_ASSOCIATE = "https://mon.adp.com/redboxapi/core/profile/v1/associates/"
URL_DETAIL_USER_WORKER = "https://mon.adp.com/hr/v2/workers/"
URL_BALANCES = "https://mon.adp.com/time/v3/workers/<USER_ID>/time-off-balances"
URL_TIMEOFF_REQUESTS = "https://mon.adp.com/time/v3/workers/<USER_ID>/time-off-requests"
URL_TIMEOFF_META = "https://mon.adp.com/events/time/v1/time-off-request.submit/meta"
URL_REFERER = "https://mon.adp.com/redbox/3.10.1.2"
URL_NEW_GITHUB_ISSUE = (
    "https://github.com/ComteHerrapait/adp_but_better/issues/new/choose"
)

LOGGING_SETTINGS_FILE = Path("logging.json")
SETTINGS_FILE = Path("config.json")
DEFAULT_SETTINGS = {
    "adp_username": "",
    "skip_password_prompt": False,
}

REGEX_USER_ID = r"[a-z]+\-\w{3}"

USER_INFO_CUSTOM_FIELD_TRANSLATIONS = {
    "collaborationType": "statut",
    "recoursReason": "recours",
    "contractType": "contrat",
    "activity": "secteur",
    "remunerationType": "salaire",
    "workSchedule": "horaire",
    "monthlyHours": "h/mois",
}


def reset_settings() -> None:
    """reset the config file to default values"""
    log.debug("settings : reset to default values")
    for k, v in DEFAULT_SETTINGS.items():
        set_setting(k, v)


def get_setting(key: str) -> Any:
    """get a setting from the config file

    Args:
        key (str): name of the setting to get

    Returns:
        Any: value of the setting
    """
    if SETTINGS_FILE.exists():
        with SETTINGS_FILE.open("r") as f:
            value = json.load(f).get(key, None)
    else:
        value = None

    if value is None:
        set_setting(key, DEFAULT_SETTINGS[key])
        value = DEFAULT_SETTINGS[key]

    log.debug(f"settings : read {key} -> {value}")

    return value


def set_setting(key: str, value: Any) -> None:
    """set the value of a setting in the config file

    Args:
        key (str): name of the setting to set
        value (Any): value of the setting
    """
    log.debug(f"settings : write {key} -> {value}")

    if SETTINGS_FILE.exists():
        with SETTINGS_FILE.open("r") as f:
            settings = json.load(f)
    else:
        settings = DEFAULT_SETTINGS

    settings[key] = value

    with SETTINGS_FILE.open("w") as f:
        json.dump(settings, f, indent=4)
