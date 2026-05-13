from datetime import date
import pytest
from nldate import parse

TODAY = date(2026, 5, 12)  # a Tuesday


def test_today() -> None:
    assert parse("today", TODAY) == TODAY


def test_tomorrow() -> None:
    assert parse("tomorrow", TODAY) == date(2026, 5, 13)


def test_yesterday() -> None:
    assert parse("yesterday", TODAY) == date(2026, 5, 11)


def test_n_days_before_date() -> None:
    assert parse("5 days before December 1st, 2026", TODAY) == date(2026, 11, 26)


def test_in_n_days() -> None:
    assert parse("in 3 days", TODAY) == date(2026, 5, 15)


def test_next_tuesday() -> None:
    assert parse("next Tuesday", TODAY) == date(2026, 5, 19)


def test_last_friday() -> None:
    assert parse("last Friday", TODAY) == date(2026, 5, 8)


def test_n_weeks_from_now() -> None:
    assert parse("2 weeks from now", TODAY) == date(2026, 5, 26)


def test_absolute_date() -> None:
    assert parse("December 1st, 2026", TODAY) == date(2026, 12, 1)


def test_invalid_raises() -> None:
    with pytest.raises(ValueError):
        parse("not a date", TODAY)


# --- singular variants ---


def test_in_1_day() -> None:
    assert parse("in 1 day", TODAY) == date(2026, 5, 13)


def test_1_day_from_now() -> None:
    assert parse("1 day from now", TODAY) == date(2026, 5, 13)


def test_1_week_from_now() -> None:
    assert parse("1 week from now", TODAY) == date(2026, 5, 19)


# --- day after / before ---


def test_day_after_tomorrow() -> None:
    assert parse("day after tomorrow", TODAY) == date(2026, 5, 14)


def test_day_before_yesterday() -> None:
    assert parse("day before yesterday", TODAY) == date(2026, 5, 10)


# --- zero edge case ---


def test_in_0_days() -> None:
    assert parse("in 0 days", TODAY) == TODAY


# --- more weekday combinations ---


def test_next_monday() -> None:
    assert parse("next Monday", TODAY) == date(2026, 5, 18)


def test_last_monday() -> None:
    assert parse("last Monday", TODAY) == date(2026, 5, 11)


def test_next_wednesday() -> None:
    assert parse("next Wednesday", TODAY) == date(2026, 5, 13)


def test_last_wednesday() -> None:
    assert parse("last Wednesday", TODAY) == date(2026, 5, 6)


# --- absolute date formats ---


def test_abbreviated_month() -> None:
    assert parse("Dec 1, 2026", TODAY) == date(2026, 12, 1)


def test_no_comma() -> None:
    assert parse("December 1 2026", TODAY) == date(2026, 12, 1)


def test_abbreviated_ordinal_no_comma() -> None:
    assert parse("Dec 1st 2026", TODAY) == date(2026, 12, 1)


# --- relative before today / yesterday ---


def test_3_days_before_today() -> None:
    assert parse("3 days before today", TODAY) == date(2026, 5, 9)


def test_1_week_before_yesterday() -> None:
    assert parse("1 week before yesterday", TODAY) == date(2026, 5, 4)


# --- case and whitespace ---


def test_whitespace() -> None:
    assert parse("  today  ", TODAY) == TODAY


def test_title_case() -> None:
    assert parse("Next Tuesday", TODAY) == date(2026, 5, 19)


def test_upper_case() -> None:
    assert parse("NEXT TUESDAY", TODAY) == date(2026, 5, 19)


# --- more absolute date formats ---


def test_iso_with_slashes() -> None:
    assert parse("2025/12/04", TODAY) == date(2025, 12, 4)


def test_iso_with_dots() -> None:
    assert parse("2025.12.04", TODAY) == date(2025, 12, 4)


def test_us_slash_format() -> None:
    assert parse("12/04/2025", TODAY) == date(2025, 12, 4)


def test_us_short_year() -> None:
    assert parse("12/04/25", TODAY) == date(2025, 12, 4)


def test_us_dash_format() -> None:
    assert parse("12-04-2025", TODAY) == date(2025, 12, 4)


def test_eu_day_before_month() -> None:
    assert parse("1 December 2026", TODAY) == date(2026, 12, 1)


def test_eu_abbreviated() -> None:
    assert parse("1 Dec 2026", TODAY) == date(2026, 12, 1)


def test_abbreviated_with_period() -> None:
    assert parse("Dec. 1, 2026", TODAY) == date(2026, 12, 1)


def test_abbreviated_period_ordinal() -> None:
    assert parse("Dec. 1st, 2026", TODAY) == date(2026, 12, 1)


def test_eu_with_period() -> None:
    assert parse("1 Dec. 2026", TODAY) == date(2026, 12, 1)


def test_eu_abbreviated_with_comma() -> None:
    assert parse("1 Dec, 2026", TODAY) == date(2026, 12, 1)


# --- more relative patterns ---


def test_n_days_ago() -> None:
    assert parse("3 days ago", TODAY) == date(2026, 5, 9)


def test_n_weeks_ago() -> None:
    assert parse("2 weeks ago", TODAY) == date(2026, 4, 28)


def test_next_week() -> None:
    assert parse("next week", TODAY) == date(2026, 5, 19)


def test_last_week() -> None:
    assert parse("last week", TODAY) == date(2026, 5, 5)


def test_the_day_after_tomorrow() -> None:
    assert parse("the day after tomorrow", TODAY) == date(2026, 5, 14)


def test_the_day_before_yesterday() -> None:
    assert parse("the day before yesterday", TODAY) == date(2026, 5, 10)


def test_in_2_weeks() -> None:
    assert parse("in 2 weeks", TODAY) == date(2026, 5, 26)


def test_in_1_week() -> None:
    assert parse("in 1 week", TODAY) == date(2026, 5, 19)


def test_days_after_date() -> None:
    assert parse("2 days after July 4, 2026", TODAY) == date(2026, 7, 6)


def test_weeks_after_date() -> None:
    assert parse("2 weeks after July 4, 2026", TODAY) == date(2026, 7, 18)


def test_week_after_today() -> None:
    assert parse("1 week after today", TODAY) == date(2026, 5, 19)


def test_days_after_yesterday() -> None:
    assert parse("3 days after yesterday", TODAY) == date(2026, 5, 14)


# --- more error cases ---


def test_empty_string_raises() -> None:
    with pytest.raises(ValueError):
        parse("", TODAY)


def test_invalid_weekday_next_raises() -> None:
    with pytest.raises(ValueError):
        parse("next foo", TODAY)


def test_invalid_weekday_last_raises() -> None:
    with pytest.raises(ValueError):
        parse("last foo", TODAY)


# --- months / years in relative ---


def test_in_3_months() -> None:
    assert parse("in 3 months", TODAY) == date(2026, 8, 12)


def test_in_1_year() -> None:
    assert parse("in 1 year", TODAY) == date(2027, 5, 12)


def test_3_months_ago() -> None:
    assert parse("3 months ago", TODAY) == date(2026, 2, 12)


def test_1_year_ago() -> None:
    assert parse("1 year ago", TODAY) == date(2025, 5, 12)


def test_3_months_from_now() -> None:
    assert parse("3 months from now", TODAY) == date(2026, 8, 12)


# --- this weekday ---


def test_this_wednesday() -> None:
    assert parse("this Wednesday", TODAY) == date(2026, 5, 13)


def test_this_tuesday() -> None:
    assert parse("this Tuesday", TODAY) == TODAY


# --- next/last month/year ---


def test_next_month() -> None:
    assert parse("next month", TODAY) == date(2026, 6, 12)


def test_last_month() -> None:
    assert parse("last month", TODAY) == date(2026, 4, 12)


def test_next_year() -> None:
    assert parse("next year", TODAY) == date(2027, 5, 12)


def test_last_year() -> None:
    assert parse("last year", TODAY) == date(2025, 5, 12)


# --- word numbers ---


def test_two_weeks_from_now() -> None:
    assert parse("two weeks from now", TODAY) == date(2026, 5, 26)


def test_three_days_ago() -> None:
    assert parse("three days ago", TODAY) == date(2026, 5, 9)


def test_a_week_from_now() -> None:
    assert parse("a week from now", TODAY) == date(2026, 5, 19)


def test_a_month_ago() -> None:
    assert parse("a month ago", TODAY) == date(2026, 4, 12)


# --- end / start of month / year ---


def test_end_of_month() -> None:
    assert parse("end of the month", TODAY) == date(2026, 5, 31)


def test_end_of_year() -> None:
    assert parse("end of the year", TODAY) == date(2026, 12, 31)


def test_start_of_month() -> None:
    assert parse("start of the month", TODAY) == date(2026, 5, 1)


def test_start_of_year() -> None:
    assert parse("start of the year", TODAY) == date(2026, 1, 1)


# --- no-year absolute dates ---


def test_december_first_no_year() -> None:
    assert parse("December 1st", TODAY) == date(2026, 12, 1)


def test_jan_1_no_year() -> None:
    assert parse("Jan 1", TODAY) == date(2026, 1, 1)


# --- of-format dates ---


def test_1st_of_january() -> None:
    assert parse("1st of January 2025", TODAY) == date(2025, 1, 1)


def test_the_1st_of_january() -> None:
    assert parse("the 1st of January", TODAY) == date(2026, 1, 1)


# --- standalone weekday ---


def test_standalone_monday() -> None:
    assert parse("monday", TODAY) == date(2026, 5, 18)


def test_standalone_tuesday() -> None:
    assert parse("tuesday", TODAY) == date(2026, 5, 19)


# --- compound offsets ---


def test_compound_after_yesterday() -> None:
    assert parse("1 year and 2 months after yesterday", TODAY) == date(2027, 7, 11)


# --- before/after with months/years ---


def test_3_months_before_date() -> None:
    assert parse("3 months before December 1st, 2026", TODAY) == date(2026, 9, 1)


def test_2_years_after_date() -> None:
    assert parse("2 years after December 1st, 2026", TODAY) == date(2028, 12, 1)


# --- invalid word number raises ---


def test_invalid_word_number_raises() -> None:
    with pytest.raises(ValueError):
        parse("in foo days", TODAY)
