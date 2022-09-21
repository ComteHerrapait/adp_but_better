import dataclasses
import os
import threading
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from json import JSONEncoder, dumps
from time import sleep, time
from typing import Any

import art
import inquirer
from requests import Session

from adp_wrapper.constants import DATE_FORMAT
from adp_wrapper.punch import get_punch_times, punch
from adp_wrapper.time_off import (
    PeriodCode,
    get_pay_codes,
    get_timeoff_requests,
    send_timeoff_request,
)
from adp_wrapper.time_processing import get_daily_stats, process_end_of_day_time

"""
These functions serve to display and interact with the user through the terminal.
"""


class EnhancedJSONEncoder(JSONEncoder):
    """Enhances the JSONEncoder class to handle dataclasses, datetime and Enum."""

    def default(self, o: Any) -> (dict[str, Any] | str | Any):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


def print_json(obj: Any, **kwargs: Any) -> None:
    """Prints a JSON representation of the given object.

    Args:
        obj (Any): object to print
        **kwargs: additional arguments passed to json.dumps
    """
    print(dumps(obj, cls=EnhancedJSONEncoder, **kwargs))


def print_header(clear: bool = True) -> None:
    """prints the app header to the terminal, using art library

    Args:
        clear (bool, optional): clear the console. Defaults to True.
    """
    if clear:
        print("\033[H\033[J", end="")
    width = os.get_terminal_size().columns
    # adapt text size to terminal width
    if width > 101:
        art.tprint("ADP but better\n", font="tarty1")
    else:
        art.tprint("ADP but better\n", font="tarty2")


def format_timedelta(timedelta: timedelta) -> str:
    """Convert a timedelta to a string.

    Args:
        timedelta (timedelta)

    Returns:
        str: formatted timedelta
    """
    days, hours, minutes = (
        timedelta.days,
        timedelta.seconds // 3600,
        (timedelta.seconds // 60) % 60,
    )
    formatted_string = ""
    if days:
        formatted_string += f"{days}d "
    if hours:
        formatted_string += f"{hours}h"
    if minutes:
        formatted_string += f"{minutes}min"
    return formatted_string


def user_validation_punch(punch_time: datetime) -> bool:
    """ask user to validate the punch time.

    Args:
        punch_time (datetime): punch date and time

    Returns:
        bool: user validated
    """
    punch_time_str = punch_time.strftime("%A(%d) %H:%M")
    validation = inquirer.confirm(f"Punching at {punch_time_str}")
    if isinstance(validation, bool):
        return validation
    else:
        return False


class Spinner:
    busy = False
    delay = 0.1
    message = "Waiting"
    start_time = 0.0
    waiting_char = "."

    def __init__(self, start_now: bool = False) -> None:
        if start_now:
            self.start()

    def task(self) -> None:
        print(self.message, end=" ")
        while self.busy:
            sleep(self.delay)
            print(self.waiting_char, end="", flush=True)
        elapsed = time() - self.start_time
        print(f" done ({elapsed:.2f}s)")

    def start(self) -> None:
        self.busy = True
        self.start_time = time()
        threading.Thread(target=self.task, name="SpinnerThread").start()

    def stop(self) -> None:
        self.busy = False
        sleep(2 * self.delay)


def display_punch_times(timestamps: list[datetime]) -> None:
    """display a list of punch times to the terminal.

    Args:
        timestamps (list[datetime]): list of punch times
            for example : today's punch times
    """
    art.tprint("\ntoday :", font="tarty2")
    print(datetime.now().strftime("%B %d %H:%M"))
    clocked_in = len(timestamps) % 2 != 0

    if timestamps:
        worked_time, remaining_time = get_daily_stats(timestamps)
        for i, timestamp in enumerate(timestamps):
            date_string, trailing_str = timestamp.strftime("%H:%M"), ""

            # process trailing info for last punch
            if i == len(timestamps) - 1:
                time_since_punch = datetime.now(timezone.utc) - timestamps[-1]
                trailing_str = f"({format_timedelta(time_since_punch)} ago)"

            print(f"{'🟢' if i % 2 == 0 else '🔴'} : {date_string} {trailing_str}")

        print()
        print(f"time worked today : {format_timedelta(worked_time)} ", end="")

        time_sign_indicator = "remaining" if (remaining_time > timedelta()) else "extra"
        print(f"({format_timedelta(remaining_time)} {time_sign_indicator})")

        end_of_day_str = process_end_of_day_time(remaining_time).strftime("%H:%M")
        print(f"your day ends at : {end_of_day_str}")

        print(f"You are clocked {'IN' if clocked_in else 'OUT'}")
    else:
        print(">> No punches today. You are clocked OUT")
    print("\n")


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


def request_time_off(session: Session) -> bool:
    # select event
    available_codes = get_pay_codes(session)
    event_code = "TTRAV2"  # TODO : ask user to select an event
    event = next((event for event in available_codes if event.code == event_code), None)
    if event is None:
        raise KeyError(f"no pay code matching the code {event_code}")

    # select start date and period
    dates_start = [date.today() + timedelta(days=i) for i in range(30)]
    questions_start = [
        inquirer.List(
            "start_date",
            message="event start date",
            choices=dates_start,
            carousel=True,
            default=dates_start[1],
        ),
        inquirer.List(
            "start_period",
            message="event start period",
            choices=["morning", "afternoon"],
            carousel=True,
        ),
    ]
    answers_start = inquirer.prompt(questions_start, raise_keyboard_interrupt=True)
    dates_end = [answers_start.get("start_date") + timedelta(days=i) for i in range(30)]
    questions_end = [
        inquirer.List(
            "end_date",
            message="event end date",
            choices=dates_end,
            carousel=True,
            default=dates_end[1],
        ),
        inquirer.List(
            "end_period",
            message="event end period",
            choices=["morning", "afternoon"],
            carousel=True,
        ),
    ]
    answers_end = inquirer.prompt(questions_end, raise_keyboard_interrupt=True)

    event.date_start = answers_start.get("start_date")
    if answers_start.get("start_period") == "morning":
        event.period_start = PeriodCode.morning
    elif answers_start.get("start_period") == "afternoon":
        event.period_start = PeriodCode.afternoon
    else:
        raise ValueError("invalid start period")

    # select end date and period
    event.date_end = answers_end.get("end_date")
    if answers_end.get("end_period") == "morning":
        event.period_end = PeriodCode.morning
    elif answers_end.get("end_period") == "afternoon":
        event.period_end = PeriodCode.afternoon
    else:
        raise ValueError("invalid end period")

    # comment
    question = [inquirer.Text("comment", message="Comment :", ignore=True)]
    comment = inquirer.prompt(question, raise_keyboard_interrupt=True)["comment"]

    # submit request
    success = send_timeoff_request(session, [event], comment)
    return success


def display_time_off_requests(session: Session) -> None:
    """display the list of time off requests.

    Args:
        session (Session): browser session
    """
    requests = get_timeoff_requests(session)
    if requests:
        for r in requests:
            date_start = r.event.date_start.strftime(DATE_FORMAT)
            date_end = r.event.date_end.strftime(DATE_FORMAT)
            period_start = r.event.period_start.value["shortName"]
            period_end = r.event.period_end.value["shortName"]
            print(f"{r.event.name} :")
            print(f"\t{date_start} {period_start} - {date_end} {period_end}")
            print(f"\t{r.status} ({r.status_date})")
        # print_json(requests, indent=2)
    else:
        print("No time off requests")
