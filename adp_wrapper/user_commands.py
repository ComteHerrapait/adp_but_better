from datetime import date, datetime, timedelta

import art
import inquirer
from requests import Session

from adp_wrapper.CLI_utils import format_timedelta, user_validation_punch
from adp_wrapper.constants import DATE_FORMAT
from adp_wrapper.punch import get_punch_times, punch
from adp_wrapper.search_user import get_users_info
from adp_wrapper.time_off import (
    PeriodCode,
    get_pay_codes,
    get_timeoff_requests,
    send_timeoff_request,
)
from adp_wrapper.time_processing import get_daily_stats


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
        time_sign_indicator = "restant" if (remaining_time > timedelta()) else "sup"
        print(f"({format_timedelta(remaining_time)} {time_sign_indicator})")

        print(f"You are clocked {'OUT' if len(timestamps) % 2 == 0 else 'IN'}")
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


def search_users(session: Session) -> list[dict]:
    """search for users in the ADP database.

    Args:
        session (Session): browser session
        search_term (str): search term

    Returns:
        list[dict]: list of users matching query
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
    return users


def request_time_off(session: Session) -> None:
    # select event
    available_codes = get_pay_codes(session)
    event_code = "TTRAV2"  # TODO : ask user to select an event
    event = next((event for event in available_codes if event.code == event_code), None)
    if event is None:
        raise Exception(f"no pay code matching the code {event_code}")

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
    answers_start = inquirer.prompt(questions_start)
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
    answers_end = inquirer.prompt(questions_end)

    event.date_start = answers_start.get("start_date")
    if answers_start.get("start_period") == "morning":
        event.period_start = PeriodCode.morning
    elif answers_start.get("start_period") == "afternoon":
        event.period_start = PeriodCode.afternoon
    else:
        raise Exception("invalid start period")

    # select end date and period
    event.date_end = answers_end.get("end_date")
    if answers_end.get("end_period") == "morning":
        event.period_end = PeriodCode.morning
    elif answers_end.get("end_period") == "afternoon":
        event.period_end = PeriodCode.afternoon
    else:
        raise Exception("invalid end period")

    # comment
    question = [inquirer.Text("comment", message="Comment :", ignore=True)]
    comment = inquirer.prompt(question)["comment"]

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