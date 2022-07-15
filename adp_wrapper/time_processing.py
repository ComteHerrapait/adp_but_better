from datetime import datetime, timedelta

from adp_wrapper.constants import DAILY_WORK_TIME


def remove_time_zone(timestamps: list[datetime]) -> list[datetime]:
    """remove time zone information from datetime objects

    Args:
        timestamps (list[datetime]): list of datetime objects

    Returns:
        list[datetime]: new list of datetime objects without time zone information
    """
    return [ts.replace(tzinfo=None) for ts in timestamps]


def fill_with_now(timestamps: list[datetime]) -> list[datetime]:
    """fills a list of datetime objects with the current time if the list is not
    complete.
    to know if the list is complete, we check if the number of elements is even.

    Args:
        timestamps (list[datetime]): list of datetime objects to complete

    Returns:
        list[datetime]: new list of datetime objects completed
    """
    if len(timestamps) % 2 != 0:
        now = datetime.now()
        now = now.replace(tzinfo=None)
        timestamps.append(now)
    return timestamps


def process_worked_time(timestamps: list[datetime]) -> timedelta:
    """processes total worked time from a list of datetime objects

    Args:
        timestamps (list[datetime]): list of punch datetime

    Returns:
        timedelta: total worked time
    """
    timestamps = remove_time_zone(timestamps)
    timestamps = fill_with_now(timestamps)
    worked_time = timedelta()

    for period_start, period_stop in zip(timestamps[0::2], timestamps[1::2]):
        worked_time += period_stop - period_start

    return worked_time


def process_time_remaining(worked_time: timedelta) -> timedelta:
    """processes work time remaining for the day from the total worked time,
    can be called balance because it can be negative if worked more the daily work time

    Args:
        worked_time (timedelta): time already worked

    Returns:
        timedelta: time left to work
    """
    return DAILY_WORK_TIME - worked_time


def get_daily_stats(timestamps: list[datetime]) -> tuple[timedelta, timedelta]:
    """gets work time done and time remaining for the day from a list of datetime objects

    Args:
        timestamps (list[datetime]): list of punch datetime

    Returns:
        tuple[timedelta, timedelta]: worked time and today's balance
    """
    worked_time = process_worked_time(timestamps)
    balance = process_time_remaining(worked_time)
    return worked_time, balance


def process_end_of_day_time(time_remaining: timedelta) -> datetime:
    """processes the hour at which your day can be considered done

    Args:
        time_remaining (timedelta): time left on your day

    Returns:
        datetime: hour of your day's end
    """

    now = datetime.now()
    end_of_day = now + time_remaining
    return end_of_day
