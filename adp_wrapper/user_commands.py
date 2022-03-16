import logging
import logging.config
from datetime import datetime
from typing import Callable

import inquirer
from requests import Session

from adp_wrapper.balance import get_balances
from adp_wrapper.CLI_utils import (
    display_time_off_requests,
    request_time_off,
    validate_and_punch,
)
from adp_wrapper.search_user import get_users_info

log = logging.getLogger(__name__)


def cmd_punch_now(session: Session) -> bool:
    punch_time = datetime.now()

    validate_and_punch(session, punch_time)
    return True


def cmd_punch_specific_time(session: Session) -> bool:
    punch_time = datetime.now()
    print("Specify punch time (values default to now)")
    hour = int(input("Hour : ") or punch_time.hour)
    minutes = int(input("Minutes : ") or punch_time.minute)
    month = int(input("Month : ") or punch_time.month)
    day = int(input("Day : ") or punch_time.day)
    try:
        punch_time = punch_time.replace(hour=hour, minute=minutes, month=month, day=day)
        validate_and_punch(session, punch_time)
    except ValueError:
        print("Cette horaire n'est pas valide")

    return True


def cmd_search_users(session: Session) -> bool:
    questions = [
        inquirer.Text(
            "query",
            message="search query",
        ),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    query = answers["query"]
    users = get_users_info(session, query)
    if not users:
        print("No users matching query found")
    for user in users:
        print(f"* {user['name']:<20} -> {user['id']}")
    return True


def cmd_get_balances(session: Session) -> bool:
    balances = get_balances(session)
    if not balances:
        print("No balance found")

    for balance in balances:
        print(f"{balance['name']:<20}: {balance['value']} ({balance['unit']})")
    return True


def cmd_request_timeoff(session: Session) -> bool:
    if request_time_off(session):
        print("Time off request successfully sent")
    else:
        print("An error occured while sending the time off request")
    return True


def cmd_get_timeoff_requests(session: Session) -> bool:
    display_time_off_requests(session)
    return True


def cmd_exit(session: Session) -> bool:
    return False


COMMAND_LIST: dict[str, Callable[[Session], bool]] = {
    "Punch now": cmd_punch_now,
    "Punch at specific time": cmd_punch_specific_time,
    "Get balance": cmd_get_balances,
    "Request time off": cmd_request_timeoff,
    "Search users": cmd_search_users,
    "Get timeoff requests": cmd_get_timeoff_requests,
    "Exit": cmd_exit,
}
