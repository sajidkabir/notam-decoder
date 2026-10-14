"""Data model for a decoded ICAO NOTAM."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Qualifier:
    """The parsed Q) qualifier line of a NOTAM."""

    fir: str                      # Flight information region, e.g. "EGTT"
    qcode: str                    # Five letter NOTAM code, e.g. "QMRXX"
    qcode_subject: str | None     # Plain words for letters 2-3, None if unknown
    qcode_condition: str | None   # Plain words for letters 4-5, None if unknown
    traffic: str                  # e.g. "IV"
    traffic_decoded: str          # e.g. "IFR and VFR traffic"
    purpose: str                  # e.g. "NBO"
    purpose_decoded: tuple[str, ...]
    scope: str                    # e.g. "A"
    scope_decoded: str            # e.g. "aerodrome"
    lower: str                    # lower limit, e.g. "000"
    upper: str                    # upper limit, e.g. "999"
    lat: float | None             # decimal degrees, None if unparseable
    lon: float | None
    radius_nm: int | None


@dataclass(frozen=True)
class Notam:
    """A fully parsed NOTAM."""

    series: str                   # Series letter, e.g. "A"
    number: int                   # NOTAM number within the series
    year: int                     # Two digit year of issue, e.g. 26
    kind: str                     # "N" (new), "R" (replacement), "C" (cancellation)
    replaces: str | None          # For NOTAMR/NOTAMC, the referenced NOTAM id
    qualifier: Qualifier
    locations: tuple[str, ...]    # Item A: ICAO indicators, e.g. ("EGLL",)
    valid_from: datetime          # Item B, UTC
    valid_to: datetime | None     # Item C, UTC; None when PERM
    permanent: bool               # Item C was "PERM"
    end_estimated: bool           # Item C carried "EST"
    schedule: str | None          # Item D raw text
    schedule_decoded: str | None  # Item D in plain words
    text: str                     # Item E raw text
    text_decoded: str             # Item E with ICAO abbreviations expanded
    lower_limit: str | None       # Item F raw
    lower_limit_decoded: str | None
    upper_limit: str | None       # Item G raw
    upper_limit_decoded: str | None
    raw: str                      # Original input, preserved verbatim
