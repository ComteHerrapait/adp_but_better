from datetime import datetime

import inquirer
from requests import Session

from adp_wrapper.auth import SessionTimeoutException, adp_login
from adp_wrapper.balance import get_balances
from adp_wrapper.CLI_utils import print_header
from adp_wrapper.constants import GOODBYE_MESSAGE
from adp_wrapper.punch import get_punch_times
from adp_wrapper.user_commands import (
    display_punch_times,
    display_time_off_requests,
    request_time_off,
    search_users,
    validate_and_punch,
)


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
                "Get Timeoff Requests",
                "Exit",
            ],
            carousel=True,
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers is not None:
        answer = answers.get("action", "Exit")
    else:
        answer = "Exit"

    match answer:
        case "Punch now":
            punch_time = datetime.now()

            validate_and_punch(session, punch_time)
            return True

        case "Punch at specific time":
            punch_time = datetime.now()
            print("Specify punch time (values default to now)")
            hour = int(input("Hour : ") or punch_time.hour)
            minutes = int(input("Minutes : ") or punch_time.minute)
            month = int(input("Month : ") or punch_time.month)
            day = int(input("Day : ") or punch_time.day)
            try:
                punch_time = punch_time.replace(
                    hour=hour, minute=minutes, month=month, day=day
                )
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

        case "Request time off":
            if request_time_off(session):
                print("Time off request successfully sent")
            else:
                print("An error occured while sending the time off request")
            return True

        case "Get Timeoff Requests":
            display_time_off_requests(session)
            return True

        case "Exit":
            return False


if __name__ == "__main__":
    # Welcome message
    print_header(True)

    # login
    session = adp_login()

    # display today's punch times
    timestamps = get_punch_times(session)
    display_punch_times(timestamps)

    running = True
    while running:
        try:
            running = main_loop(session)
        except SessionTimeoutException:
            print_header(True)
            print("Session timed out. Logging in again...")
            session = adp_login()
            timestamps = get_punch_times(session)
            display_punch_times(timestamps)
        except KeyboardInterrupt:
            print("Program interrupted")
            running = False

    exit(GOODBYE_MESSAGE)
