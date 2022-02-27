from datetime import datetime, timedelta

from adp_wrapper.constants import DAILY_WORK_TIME


def remove_time_zone(timestamps: list[datetime]) -> list[datetime]:
    return [ts.replace(tzinfo=None) for ts in timestamps]


def fill_with_now(timestamps: list[datetime]) -> list[datetime]:
    if len(timestamps) % 2 != 0:
        now = datetime.now()
        now = now.replace(tzinfo=None)
        timestamps.append(now)
    return timestamps


def process_worked_time(timestamps: list[datetime]) -> timedelta:
    timestamps = remove_time_zone(timestamps)
    timestamps = fill_with_now(timestamps)
    worked_time = timedelta()

    for period_start, period_stop in zip(timestamps[0::2], timestamps[1::2]):
        worked_time += period_stop - period_start

    return worked_time


def process_time_remaining(worked_time: timedelta) -> timedelta:
    return DAILY_WORK_TIME - worked_time


def get_daily_stats(timestamps: list[datetime]) -> tuple[timedelta, timedelta]:
    worked_time = process_worked_time(timestamps)
    balance = process_time_remaining(worked_time)
    return worked_time, balance
