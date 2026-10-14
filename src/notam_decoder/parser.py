"""Parser for ICAO format NOTAMs (Annex 15 style)."""

from __future__ import annotations

import re
from datetime import datetime, timezone

from .abbreviations import expand
from .models import Notam, Qualifier
from .qcodes import (
    decode_condition,
    decode_purpose,
    decode_scope,
    decode_subject,
    decode_traffic,
)
from .schedule import decode_level, decode_schedule

_HEADER_RE = re.compile(
    r"\(?\s*([A-Z])(\d{4})/(\d{2})\s+NOTAM([NRC])(?:\s+([A-Z]?\d{4}/\d{2}))?"
)
_ITEM_RE = re.compile(r"(?:^|\s)([A-GQ])\)\s*")
_TIME_RE = re.compile(r"^(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$")
_QCOORD_RE = re.compile(r"^(\d{4})([NS])(\d{5})([EW])(\d{3})$")


class NotamParseError(ValueError):
    """Raised when input is not a parseable ICAO NOTAM."""


def _parse_time(group: str) -> datetime:
    match = _TIME_RE.match(group.strip())
    if match is None:
        raise NotamParseError(f"bad date-time group: {group!r}")
    yy, mo, dd, hh, mm = (int(g) for g in match.groups())
    year = 1900 + yy if yy >= 69 else 2000 + yy
    try:
        return datetime(year, mo, dd, hh, mm, tzinfo=timezone.utc)
    except ValueError as exc:
        raise NotamParseError(f"bad date-time group: {group!r}") from exc


def _parse_qcoord(field: str) -> tuple[float | None, float | None, int | None]:
    match = _QCOORD_RE.match(field.strip())
    if match is None:
        return None, None, None
    lat_raw, lat_hemi, lon_raw, lon_hemi, radius = match.groups()
    lat = int(lat_raw[:2]) + int(lat_raw[2:]) / 60.0
    lon = int(lon_raw[:3]) + int(lon_raw[3:]) / 60.0
    if lat_hemi == "S":
        lat = -lat
    if lon_hemi == "W":
        lon = -lon
    return round(lat, 6), round(lon, 6), int(radius)


def _split_items(body: str) -> dict[str, str]:
    """Split the NOTAM body into its A) to G) items."""
    marks = list(_ITEM_RE.finditer(body))
    if not marks:
        raise NotamParseError("no A) to G) items found")
    items: dict[str, str] = {}
    for i, mark in enumerate(marks):
        letter = mark.group(1)
        start = mark.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        items[letter] = body[start:end].strip().rstrip(")")
    return items


def _parse_qualifier(text: str) -> Qualifier:
    fields = text.split("/")
    if len(fields) != 8:
        raise NotamParseError(
            f"Q) line must have 8 slash-separated fields, got {len(fields)}"
        )
    fir, qcode, traffic, purpose, scope, lower, upper, coord = (
        f.strip() for f in fields
    )
    lat, lon, radius = _parse_qcoord(coord)
    return Qualifier(
        fir=fir,
        qcode=qcode,
        qcode_subject=decode_subject(qcode),
        qcode_condition=decode_condition(qcode),
        traffic=traffic,
        traffic_decoded=decode_traffic(traffic) or traffic,
        purpose=purpose,
        purpose_decoded=decode_purpose(purpose) or (purpose,),
        scope=scope,
        scope_decoded=decode_scope(scope) or scope,
        lower=lower,
        upper=upper,
        lat=lat,
        lon=lon,
        radius_nm=radius,
    )


def parse_notam(text: str) -> Notam:
    """Parse one ICAO NOTAM from text.

    Accepts the full message including surrounding parentheses and line
    breaks, or just the item text. Raises NotamParseError on bad input.
    """
    raw = text
    head = _HEADER_RE.search(text)
    if head is None:
        raise NotamParseError(
            "no NOTAM header found (expected e.g. 'A1912/15 NOTAMN')"
        )
    series, number, year, kind, replaces = head.groups()
    items = _split_items(text[head.end():])
    if "Q" not in items:
        raise NotamParseError("Q) qualifier line is required")
    if "A" not in items:
        raise NotamParseError("A) location item is required")
    if "B" not in items:
        raise NotamParseError("B) validity start is required")
    if "E" not in items:
        raise NotamParseError("E) text item is required")

    qualifier = _parse_qualifier(items["Q"])
    locations = tuple(items["A"].split())

    valid_from = _parse_time(items["B"])

    c_raw = items.get("C", "").strip()
    permanent = c_raw.upper() == "PERM"
    end_estimated = c_raw.upper().endswith("EST")
    if permanent:
        valid_to = None
    else:
        valid_to = _parse_time(c_raw[:-3].strip() if end_estimated else c_raw)

    schedule_raw = items.get("D")
    schedule_decoded = decode_schedule(schedule_raw) if schedule_raw else None

    lower_raw = items.get("F")
    upper_raw = items.get("G")

    return Notam(
        series=series,
        number=int(number),
        year=int(year),
        kind=kind,
        replaces=replaces,
        qualifier=qualifier,
        locations=locations,
        valid_from=valid_from,
        valid_to=valid_to,
        permanent=permanent,
        end_estimated=end_estimated,
        schedule=schedule_raw,
        schedule_decoded=schedule_decoded,
        text=items["E"],
        text_decoded=expand(items["E"]),
        lower_limit=lower_raw,
        lower_limit_decoded=decode_level(lower_raw) if lower_raw else None,
        upper_limit=upper_raw,
        upper_limit_decoded=decode_level(upper_raw) if upper_raw else None,
        raw=raw,
    )
