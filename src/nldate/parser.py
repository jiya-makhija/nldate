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


def _parse_absolute_date(s: str) -> date | None:
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", s)
    cleaned = re.sub(
        r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.",
        r"\1",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    for fmt in (
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
    ):
        try:
            from datetime import datetime

            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None


def _resolve_relative(s: str, today: date) -> date | None:
    if s == "today":
        return today
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "tomorrow":
        return today + timedelta(days=1)
    return None


def _resolve_before(target: str, today: date, n: int) -> date:
    rel = _resolve_relative(target, today)
    if rel is not None:
        return rel - timedelta(days=n)
    abs_date = _parse_absolute_date(target)
    if abs_date is not None:
        return abs_date - timedelta(days=n)
    raise ValueError(f"Could not parse date before {target}")


def _resolve_after(target: str, today: date, n: int) -> date:
    rel = _resolve_relative(target, today)
    if rel is not None:
        return rel + timedelta(days=n)
    abs_date = _parse_absolute_date(target)
    if abs_date is not None:
        return abs_date + timedelta(days=n)
    raise ValueError(f"Could not parse date after {target}")


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip()

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

    m = re.match(r"in (\d+) days?$", s, re.IGNORECASE)
    if m:
        return today + timedelta(days=int(m.group(1)))

    m = re.match(r"in (\d+) weeks?$", s, re.IGNORECASE)
    if m:
        return today + timedelta(weeks=int(m.group(1)))

    m = re.match(r"(\d+) days? from now$", s, re.IGNORECASE)
    if m:
        return today + timedelta(days=int(m.group(1)))

    m = re.match(r"(\d+) weeks? from now$", s, re.IGNORECASE)
    if m:
        return today + timedelta(weeks=int(m.group(1)))

    m = re.match(r"(\d+) days? ago$", s, re.IGNORECASE)
    if m:
        return today - timedelta(days=int(m.group(1)))

    m = re.match(r"(\d+) weeks? ago$", s, re.IGNORECASE)
    if m:
        return today - timedelta(weeks=int(m.group(1)))

    m = re.match(r"(\d+) days? before (.+)$", s, re.IGNORECASE)
    if m:
        return _resolve_before(m.group(2).strip(), today, int(m.group(1)))

    m = re.match(r"(\d+) weeks? before (.+)$", s, re.IGNORECASE)
    if m:
        return _resolve_before(m.group(2).strip(), today, int(m.group(1)) * 7)

    m = re.match(r"(\d+) days? after (.+)$", s, re.IGNORECASE)
    if m:
        return _resolve_after(m.group(2).strip(), today, int(m.group(1)))

    m = re.match(r"(\d+) weeks? after (.+)$", s, re.IGNORECASE)
    if m:
        return _resolve_after(m.group(2).strip(), today, int(m.group(1)) * 7)

    m = re.match(r"next (\w+)$", s, re.IGNORECASE)
    if m:
        try:
            target = WEEKDAYS.index(m.group(1).lower())
        except ValueError:
            raise ValueError(f"Could not parse date: {s}")
        current = today.weekday()
        days_ahead = (target - current + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    m = re.match(r"last (\w+)$", s, re.IGNORECASE)
    if m:
        try:
            target = WEEKDAYS.index(m.group(1).lower())
        except ValueError:
            raise ValueError(f"Could not parse date: {s}")
        current = today.weekday()
        days_behind = (current - target + 7) % 7
        if days_behind == 0:
            days_behind = 7
        return today - timedelta(days=days_behind)

    abs_date = _parse_absolute_date(s)
    if abs_date is not None:
        return abs_date

    raise ValueError(f"Could not parse date: {s}")
