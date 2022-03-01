from datetime import datetime, timedelta

import art
import inquirer
from requests import Session

from adp_wrapper.punch import get_punch_times, punch
from adp_wrapper.search_user import get_users_info
from adp_wrapper.time_processing import get_daily_stats

"""
These functions serve to display and interact with the user through the terminal.
"""


def print_header(clear: bool = True) -> None:
    """prints the app header to the terminal, using art library

    Args:
        clear (bool, optional): clear the console. Defaults to True.
    """
    if clear:
        print("\033[H\033[J", end="")
    art.tprint("ADP but better\n", font="tarty1")


def format_timedelta(timedelta: timedelta) -> str:
    """Convert a timedelta to a string.

    Args:
        timedelta (timedelta)

    Returns:
        str: formatted timedelta
    """
    return str(abs(timedelta))[:-3]


def display_punch_times(timestamps: list[datetime]) -> None:
    """display a list of punch times to the terminal.

    Args:
        timestamps (list[datetime]): list of punch times
            for example : today's punch times
    """
    art.tprint("\ntoday :", font="tarty2")

    if timestamps:
        worked_time, remaining_time = get_daily_stats(timestamps)
        for i, timestamp in enumerate(timestamps):
            date_string = timestamp.strftime("%H:%M")
            print(f"{'🟢' if i % 2 == 0 else '🔴'} : {date_string}")

        print(f">> {len(timestamps)} punches today. ")
        print(f"time worked today : {format_timedelta(worked_time)} ", end="")
        time_sign_indicator = {"restant" if (remaining_time > timedelta()) else "sup"}
        print(f"({format_timedelta(remaining_time)} {time_sign_indicator})")

        print(f"You are clocked {'OUT' if len(timestamps) % 2 == 0 else 'IN'}")
    else:
        print(">> No punches today. You are clocked OUT")
    print("\n")


def user_validation_punch(punch_time: datetime) -> bool:
    """ask user to validate the punch time.

    Args:
        punch_time (datetime): punch date and time

    Returns:
        bool: user validated
    """
    punch_time_str = punch_time.strftime("%A(%d) %H:%M")
    return inquirer.confirm(f"Punching at {punch_time_str}")


def validate_and_punch(session: Session, punch_time: datetime) -> None:
    """validate the punch time and sends the requests.

    Args:
        session (Session): browser session
        punch_time (datetime): punch date and time
    """
    if user_validation_punch(punch_time):
        if punch(session, punch_time):
            print("Punch successfully sent")
            timestamps = get_punch_times(session)
            display_punch_times(timestamps)
        else:
            print("Punch failed")
    else:
        print("Punch cancelled")


def search_users(session: Session) -> None:
    """search for users in the ADP database.

    Args:
        session (Session): browser session
        search_term (str): search term
    """
    questions = [
        inquirer.Text(
            "query",
            message="search query",
        ),
    ]
    answers = inquirer.prompt(questions)
    query = answers["query"]
    users = get_users_info(session, query)
    for user in users:
        print(f"* {user['name']:<20} -> {user['id']}")
