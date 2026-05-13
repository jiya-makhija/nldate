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
