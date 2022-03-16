from datetime import datetime, timedelta
from random import randint
from typing import List

import pytest
from adp_wrapper.constants import DAILY_WORK_TIME
from adp_wrapper.time_processing import (
    fill_with_now,
    process_time_remaining,
    process_worked_time,
    remove_time_zone,
)


class TestRemoveTimeZone:
    def test_multi(self) -> None:
        before = datetime.now()
        expected = before.replace(tzinfo=None)

        after = remove_time_zone([before, before, before])
        assert after == [expected, expected, expected]

    def test_single(self) -> None:
        before = datetime.now()
        expected = before.replace(tzinfo=None)

        after = remove_time_zone([before])
        assert after == [expected]


class TestFillWithNow:
    def test_fill_from_one(self) -> None:
        before = [datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)]
        after = fill_with_now(before)
        assert len(after) == 2

    def test_fill_from_two(self) -> None:
        before = [
            datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0),
            datetime(year=1970, month=5, day=5, hour=0, minute=0, second=0),
        ]
        after = fill_with_now(before)
        assert len(after) == 2

    def test_fill_from_empty(self) -> None:
        before: List[datetime] = []
        after = fill_with_now(before)
        assert len(after) == 0


class TestProcessWorkedTime:
    @pytest.mark.parametrize("execution_number", range(5))
    def test_two_datetime(self, execution_number: int) -> None:
        # execution_number is used to run the test multiple times
        timestamps = [
            datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0),
            datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0),
        ]
        expected = timedelta(minutes=randint(0, 60), hours=randint(0, 24))
        timestamps[1] += expected

        worked_time = process_worked_time(timestamps)
        assert worked_time == expected


class TestProcessTimeRemaining:
    def test_time_remaining_zero(self) -> None:
        assert process_time_remaining(DAILY_WORK_TIME) == timedelta()

    def test_37_hours_per_week(self) -> None:
        weekly_day_count = 5
        weekly_work_time = timedelta(hours=37).total_seconds()
        actual_weekly_work_time = DAILY_WORK_TIME.total_seconds() * weekly_day_count
        assert weekly_work_time == actual_weekly_work_time
