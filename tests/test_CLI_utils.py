from datetime import timedelta

from adp_wrapper.CLI_utils import format_timedelta



class TestFormatTimeDelta:
    def test_all_fields(self) -> None:
        input = timedelta(days=1, hours=2,minutes=3,seconds=4)
        output = format_timedelta(input)

        assert output == "1d 2h03"

    def test_all_fields_negative(self) -> None:
        input = - timedelta(days=1, hours=2,minutes=3,seconds=4)
        output = format_timedelta(input)

        assert output == "1d 2h03"

    def test_only_days(self) -> None:
        input = timedelta(days=3)
        output = format_timedelta(input)

        assert output == "3 days"

    def test_only_hours(self) -> None:
        input = timedelta(hours=3)
        output = format_timedelta(input)

        assert output == "3 hours"

    def test_only_minutes(self) -> None:
        input = timedelta(minutes=3)
        output = format_timedelta(input)

        assert output == "3 min"

    def test_zero(self) -> None:
        input = timedelta()
        output = format_timedelta(input)

        assert output == ""

    def test_days_and_hours(self) -> None:
        input = timedelta(days=8, hours=3)
        output = format_timedelta(input)

        assert output == "8d 3h00"

    def test_days_and_minutes(self) -> None:
        input = timedelta(days=8, minutes=3)
        output = format_timedelta(input)

        assert output == "8d 0h03"

    def test_hours_and_minutes(self) -> None:
        input = timedelta(hours=7, minutes=43)
        output = format_timedelta(input)

        assert output == "7h43"

