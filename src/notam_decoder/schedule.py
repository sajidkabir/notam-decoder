"""Decoding of NOTAM item D schedules and items F/G height limits."""

import re

_DAYS = {
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
    "SAT": "Saturday",
    "SUN": "Sunday",
}

_DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def _day_range(token: str) -> str | None:
    """Decode a MON-FRI style range; None if the token is not one."""
    if "-" not in token:
        return None
    first, last = token.split("-", 1)
    first, last = first.strip(), last.strip()
    if first in _DAY_ORDER and last in _DAY_ORDER:
        if first == last:
            return _DAYS[first]
        return f"{_DAYS[first]} to {_DAYS[last]}"
    return None


def decode_schedule(text: str) -> str:
    """Turn an item D schedule line into plain words.

    Unknown tokens pass through unchanged.
    """
    tokens = text.replace(",", " ").split()
    out: list[str] = []
    for token in tokens:
        out.append(_decode_schedule_token(token))
    return " ".join(out)


_SIMPLE_SCHEDULE = {
    "DAILY": "daily",
    "EXC": "except",
    "H24": "24 hours",
    "HX": "no specific working hours",
    "SR": "sunrise",
    "SS": "sunset",
    "FM": "from",
    "FROM": "from",
    "TIL": "until",
    "TL": "until",
    "BTN": "between",
}


def _decode_schedule_word(word: str) -> str | None:
    """Decode one schedule word; None when unknown."""
    upper = word.upper().strip("()")
    if upper in _DAYS:
        return _DAYS[upper]
    if upper in _SIMPLE_SCHEDULE:
        return _SIMPLE_SCHEDULE[upper]
    if re.fullmatch(r"\d{4}", upper):
        return f"{upper[:2]}:{upper[2:]} UTC"
    return None


def _decode_schedule_token(token: str) -> str:
    """Decode one schedule token, handling X-Y ranges."""
    day_range = _day_range(token)
    if day_range is not None:
        return day_range
    if "-" in token:
        parts = [_decode_schedule_word(p) for p in token.split("-")]
        if all(parts):
            if all(p.endswith(" UTC") for p in parts):
                parts = [p[: -len(" UTC")] for p in parts]
                return " to ".join(parts) + " UTC"
            return " to ".join(parts)
        return token
    plain = _decode_schedule_word(token)
    return plain if plain is not None else token


_LEVEL_RE = re.compile(
    r"^(?:(?P<fl>FL)(\d{1,3})|(?P<ft>\d+)\s?FT|(?P<sfc>SFC)|(?P<gnd>GND))$"
)


def decode_level(text: str) -> str:
    """Turn an item F/G height limit into plain words.

    Handles SFC, GND, FLnnn, and nnnnFT, with an optional AMSL/AGL datum
    suffix. Anything else passes through unchanged.
    """
    raw = text.strip().upper()
    datum = ""
    for suffix, plain in ((" AMSL", " above mean sea level"),
                          (" AGL", " above ground level")):
        if raw.endswith(suffix):
            datum = plain
            raw = raw[: -len(suffix)].strip()
            break
    match = _LEVEL_RE.match(raw)
    if match is None:
        return text.strip()
    if match.group("sfc"):
        return "surface" + datum
    if match.group("gnd"):
        return "ground" + datum
    if match.group("fl"):
        return f"flight level {int(match.group(2))}" + datum
    return f"{int(match.group('ft'))} feet" + datum
