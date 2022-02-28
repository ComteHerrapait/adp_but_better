from datetime import datetime

import inquirer
from requests import Session

from adp_wrapper.auth import adp_login
from adp_wrapper.CLI_utils import display_punch_times, print_header, validate_and_punch
from adp_wrapper.constants import GOODBYE_MESSAGE
from adp_wrapper.punch import get_punch_times


def main_loop(session: Session):
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do now ?",
            choices=["Punch now", "Punch at specific time", "Exit"],
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

    while main_loop(session):
        print_header(False)

    exit(GOODBYE_MESSAGE)
