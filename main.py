from datetime import datetime

import inquirer
from requests import Session

from adp_wrapper.auth import adp_login
from adp_wrapper.balance import get_balances
from adp_wrapper.CLI_utils import (
    display_punch_times,
    print_header,
    request_time_off,
    search_users,
    validate_and_punch,
)
from adp_wrapper.constants import GOODBYE_MESSAGE
from adp_wrapper.punch import get_punch_times


def main_loop(session: Session):
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do now ?",
            choices=[
                "Punch now",
                "Punch at specific time",
                "Get balance",
                "Request time off",
                "Search users",
                "Exit",
            ],
            carousel=True,
        ),
    ]
    match inquirer.prompt(questions).get("action"):
        case "Punch now":
            punch_time = datetime.now()

            validate_and_punch(session, punch_time)
            return True

        case "Punch at specific time":
            punch_time = datetime.now()
            hour = int(input("Hour : ") or punch_time.hour)
            minutes = int(input("Minutes : ") or punch_time.minute)
            try:
                punch_time = punch_time.replace(hour=hour, minute=minutes)
            except ValueError:
                print("Cette horaire n'est pas valide")
                return True

            validate_and_punch(session, punch_time)
            return True

        case "Search users":
            users = search_users(session)
            if not users:
                print("No users matching query found")
            for user in users:
                print(f"* {user['name']:<20} -> {user['id']}")
            return True

        case "Get balance":
            balances = get_balances(session)
            if not balances:
                print("No balance found")

            for balance in balances:
                print(f"{balance['name']:<20}: {balance['value']} ({balance['unit']})")
            return True

        case "Exit":
            return False

        case "Request time off":
            if request_time_off(session):
                print("Time off request successfully sent")
            else:
                print("An error occured while sending the time off request")
            return True


if __name__ == "__main__":
    # Welcome message
    print_header(True)

    # login
    session = adp_login()

    # display today's punch times
    timestamps = get_punch_times(session)
    display_punch_times(timestamps)

    while main_loop(session):
        print_header(False)

    exit(GOODBYE_MESSAGE)
