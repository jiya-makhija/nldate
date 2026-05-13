import calendar
import re
from datetime import date, timedelta

WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

WORD_NUMBERS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "a": 1,
    "an": 1,
}

_UNIT_ALIASES = {
    "day": "days",
    "days": "days",
    "week": "weeks",
    "weeks": "weeks",
    "month": "months",
    "months": "months",
    "year": "years",
    "years": "years",
}


def _parse_number(s: str) -> int | None:
    s = s.strip().lower()
    try:
        return int(s)
    except ValueError:
        return WORD_NUMBERS.get(s)


def _add_months(d: date, n: int) -> date:
    total = d.month - 1 + n
    year = d.year + total // 12
    month = total % 12 + 1
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(d.day, max_day))


def _apply_offset(d: date, n: int, unit: str) -> date:
    if unit == "days":
        return d + timedelta(days=n)
    if unit == "weeks":
        return d + timedelta(weeks=n)
    if unit == "months":
        return _add_months(d, n)
    if unit == "years":
        return _add_months(d, n * 12)
    raise ValueError(f"Unknown unit: {unit}")


def _next_weekday(
    from_date: date, target_weekday: int, allow_today: bool = False
) -> date:
    current = from_date.weekday()
    days_ahead = (target_weekday - current + 7) % 7
    if days_ahead == 0 and not allow_today:
        days_ahead = 7
    return from_date + timedelta(days=days_ahead)


def _prev_weekday(from_date: date, target_weekday: int) -> date:
    current = from_date.weekday()
    days_behind = (current - target_weekday + 7) % 7
    if days_behind == 0:
        days_behind = 7
    return from_date - timedelta(days=days_behind)


def _resolve_relative(s: str, today: date) -> date | None:
    if s == "today":
        return today
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "tomorrow":
        return today + timedelta(days=1)
    return None


def _resolve_before(target: str, today: date, n: int, unit: str = "days") -> date:
    rel = _resolve_relative(target, today)
    if rel is not None:
        return _apply_offset(rel, -n, unit)
    abs_date = _parse_absolute_date(target, today)
    if abs_date is not None:
        return _apply_offset(abs_date, -n, unit)
    raise ValueError(f"Could not parse date before {target}")


def _resolve_after(target: str, today: date, n: int, unit: str = "days") -> date:
    rel = _resolve_relative(target, today)
    if rel is not None:
        return _apply_offset(rel, n, unit)
    abs_date = _parse_absolute_date(target, today)
    if abs_date is not None:
        return _apply_offset(abs_date, n, unit)
    raise ValueError(f"Could not parse date after {target}")


def _clean_absolute(s: str) -> str:
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", s)
    cleaned = re.sub(
        r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.",
        r"\1",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"^the\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(\d+)\s+of\s+", r"\1 ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


_ABS_FMTS_WITH_YEAR = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%m-%d-%Y",
    "%m-%d-%y",
    "%m.%d.%Y",
    "%m.%d.%y",
    "%B %d, %Y",
    "%B %d %Y",
    "%b %d, %Y",
    "%b %d %Y",
    "%d %B %Y",
    "%d %b %Y",
    "%d %B, %Y",
    "%d %b, %Y",
]

_ABS_FMTS_NO_YEAR = [
    "%B %d",
    "%b %d",
    "%d %B",
    "%d %b",
]


def _parse_absolute_date(s: str, today: date | None = None) -> date | None:
    cleaned = _clean_absolute(s)

    from datetime import datetime

    for fmt in _ABS_FMTS_WITH_YEAR:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue

    if today is not None:
        for fmt in _ABS_FMTS_NO_YEAR:
            try:
                dt = datetime.strptime(cleaned, fmt)
                return date(today.year, dt.month, dt.day)
            except ValueError:
                continue

    return None


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip()

    # --- exact phrases ---
    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today - timedelta(days=1)
    if s in ("day after tomorrow", "the day after tomorrow"):
        return today + timedelta(days=2)
    if s in ("day before yesterday", "the day before yesterday"):
        return today - timedelta(days=2)

    if s == "next week":
        return today + timedelta(weeks=1)
    if s == "last week":
        return today - timedelta(weeks=1)
    if s == "next month":
        return _add_months(today, 1)
    if s == "last month":
        return _add_months(today, -1)
    if s == "next year":
        return _add_months(today, 12)
    if s == "last year":
        return _add_months(today, -12)

    if s in ("end of the month", "end of month"):
        last_day = calendar.monthrange(today.year, today.month)[1]
        return date(today.year, today.month, last_day)
    if s in ("start of the month", "start of month"):
        return date(today.year, today.month, 1)
    if s in ("end of the year", "end of year"):
        return date(today.year, 12, 31)
    if s in ("start of the year", "start of year"):
        return date(today.year, 1, 1)

    # --- in N unit ---
    m = re.match(r"in (\S+) (days?|weeks?|months?|years?)$", s, re.IGNORECASE)
    if m:
        n = _parse_number(m.group(1))
        if n is not None:
            unit = _UNIT_ALIASES[m.group(2).lower()]
            return _apply_offset(today, n, unit)
        raise ValueError(f"Could not parse date: {s}")

    # --- N unit ago ---
    m = re.match(r"(\S+) (days?|weeks?|months?|years?) ago$", s, re.IGNORECASE)
    if m:
        n = _parse_number(m.group(1))
        if n is not None:
            unit = _UNIT_ALIASES[m.group(2).lower()]
            return _apply_offset(today, -n, unit)
        raise ValueError(f"Could not parse date: {s}")

    # --- N unit from now ---
    m = re.match(r"(\S+) (days?|weeks?|months?|years?) from now$", s, re.IGNORECASE)
    if m:
        n = _parse_number(m.group(1))
        if n is not None:
            unit = _UNIT_ALIASES[m.group(2).lower()]
            return _apply_offset(today, n, unit)
        raise ValueError(f"Could not parse date: {s}")

    # --- N unit before target ---
    m = re.match(r"(\S+) (days?|weeks?|months?|years?) before (.+)$", s, re.IGNORECASE)
    if m:
        n = _parse_number(m.group(1))
        if n is not None:
            unit = _UNIT_ALIASES[m.group(2).lower()]
            return _resolve_before(m.group(3).strip(), today, n, unit)
        raise ValueError(f"Could not parse date: {s}")

    # --- N unit after target ---
    m = re.match(r"(\S+) (days?|weeks?|months?|years?) after (.+)$", s, re.IGNORECASE)
    if m:
        n = _parse_number(m.group(1))
        if n is not None:
            unit = _UNIT_ALIASES[m.group(2).lower()]
            return _resolve_after(m.group(3).strip(), today, n, unit)
        raise ValueError(f"Could not parse date: {s}")

    # --- general compound: multiple N-unit pairs before/after target ---
    # Handles: "2 years, 3 months before X", "1 year and 2 months after X",
    #          "2 years, 3 months, 1 day before X", etc.
    m = re.match(r"(.+)\s+(before|after)\s+(.+)$", s, re.IGNORECASE)
    if m:
        offset_str = m.group(1).strip()
        direction = m.group(2).lower()
        target = m.group(3).strip()

        cleaned_offset = re.sub(r"[,\s]+and\s+", " ", offset_str)
        cleaned_offset = re.sub(r",", " ", cleaned_offset)
        cleaned_offset = re.sub(r"\s+", " ", cleaned_offset).strip()

        pairs = re.findall(
            r"(\S+)\s+(years?|months?|weeks?|days?)", cleaned_offset, re.IGNORECASE
        )

        if len(pairs) >= 2:
            total_months = 0
            total_days = 0
            valid = True
            for num_str, unit_str in pairs:
                n = _parse_number(num_str)
                if n is None:
                    valid = False
                    break
                u: str | None = _UNIT_ALIASES.get(unit_str.lower())
                if u is None:
                    valid = False
                    break
                if u == "years":
                    total_months += n * 12
                elif u == "months":
                    total_months += n
                elif u == "weeks":
                    total_days += n * 7
                elif u == "days":
                    total_days += n

            if valid:
                base: date | None = _resolve_relative(target, today)
                if base is None:
                    base = _parse_absolute_date(target, today)

                if base is not None:
                    if direction == "before":
                        result = _add_months(base, -total_months)
                        result -= timedelta(days=total_days)
                    else:
                        result = _add_months(base, total_months)
                        result += timedelta(days=total_days)
                    return result

            raise ValueError(f"Could not parse date: {s}")

    # --- this WEEKDAY ---
    m = re.match(r"this (\w+)$", s, re.IGNORECASE)
    if m:
        try:
            target = WEEKDAYS.index(m.group(1).lower())
            return _next_weekday(today, target, allow_today=True)
        except ValueError:
            raise ValueError(f"Could not parse date: {s}")

    # --- next WEEKDAY ---
    m = re.match(r"next (\w+)$", s, re.IGNORECASE)
    if m:
        try:
            target = WEEKDAYS.index(m.group(1).lower())
            return _next_weekday(today, target, allow_today=False)
        except ValueError:
            raise ValueError(f"Could not parse date: {s}")

    # --- last WEEKDAY ---
    m = re.match(r"last (\w+)$", s, re.IGNORECASE)
    if m:
        try:
            target = WEEKDAYS.index(m.group(1).lower())
            return _prev_weekday(today, target)
        except ValueError:
            raise ValueError(f"Could not parse date: {s}")

    # --- standalone weekday (assume next occurrence) ---
    try:
        target = WEEKDAYS.index(s.lower())
        return _next_weekday(today, target, allow_today=False)
    except ValueError:
        pass

    # --- absolute date ---
    abs_date = _parse_absolute_date(s, today)
    if abs_date is not None:
        return abs_date

    raise ValueError(f"Could not parse date: {s}")
