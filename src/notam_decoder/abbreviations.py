"""ICAO abbreviation expansion for NOTAM item E text.

Based on ICAO Doc 8400. Expansion is token based and case insensitive:
only whole tokens expand, so "RUNWAY09" stays untouched while "RWY"
becomes "runway". Tokens containing digits or slashes (like "09R/27L"
or "U/S") are matched exactly first, then plain alphabetic tokens.
"""

ABBREVIATIONS: dict[str, str] = {
    # aerodrome and movement area
    "AD": "aerodrome",
    "RWY": "runway",
    "THR": "threshold",
    "TWY": "taxiway",
    "APN": "apron",
    "APRON": "apron",
    "CLSD": "closed",
    "WIP": "work in progress",
    "AVBL": "available",
    "U/S": "unserviceable",
    "UNSER": "unserviceable",
    "OPR": "operating",
    "OPS": "operations",
    "OPN": "open",
    "TEMPO": "temporarily",
    "TEMP": "temporary",
    "PERM": "permanent",
    "EST": "estimated",
    # procedures and phases of flight
    "APCH": "approach",
    "DEP": "departure",
    "ARR": "arrival",
    "TKOF": "take-off",
    "LDG": "landing",
    "TFC": "traffic",
    "GA": "general aviation",
    "VFR": "visual flight rules",
    "IFR": "instrument flight rules",
    "ACFT": "aircraft",
    "HEL": "helicopter",
    "UAS": "unmanned aircraft system",
    "UAV": "unmanned aerial vehicle",
    # airspace
    "FIR": "flight information region",
    "UIR": "upper flight information region",
    "CTA": "control area",
    "CTR": "control zone",
    "TMA": "terminal control area",
    "ATZ": "aerodrome traffic zone",
    "TSA": "temporary segregated area",
    "TRA": "temporary reserved area",
    "DNG": "danger",
    "DANGER": "danger area",
    "REST": "restricted",
    "PROHIB": "prohibited",
    # services and publications
    "ATS": "air traffic services",
    "ATC": "air traffic control",
    "AIS": "aeronautical information service",
    "ARO": "air traffic services reporting office",
    "AIP": "aeronautical information publication",
    "AIC": "aeronautical information circular",
    "SUP": "supplement",
    "NOTAM": "notice to airmen",
    "PIB": "pre-flight information bulletin",
    "SNOWTAM": "snow notice to airmen",
    "ASHTAM": "ash notice to airmen",
    "BIRDTAM": "bird notice to airmen",
    # navigation aids and lighting
    "ILS": "instrument landing system",
    "LOC": "localizer",
    "GP": "glide path",
    "DME": "distance measuring equipment",
    "VOR": "VHF omnidirectional range",
    "NDB": "non-directional beacon",
    "PAPI": "precision approach path indicator",
    "ALS": "approach lighting system",
    "SALS": "simple approach lighting system",
    "TDZ": "touchdown zone",
    "RVR": "runway visual range",
    "LGT": "light",
    "LGTD": "lighted",
    "LGTN": "lightning",
    # meteorology and time
    "MET": "meteorological",
    "VIS": "visibility",
    "BRG": "bearing",
    "SR": "sunrise",
    "SS": "sunset",
    "HX": "no specific working hours",
    "H24": "24 hour service",
    "DLY": "daily",
    "EXC": "except",
    "BTN": "between",
    "FM": "from",
    "TIL": "until",
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
    "SAT": "Saturday",
    "SUN": "Sunday",
    # units and quantities
    "FT": "feet",
    "M": "metres",
    "KM": "kilometres",
    "NM": "nautical miles",
    "KT": "knots",
    "FL": "flight level",
    "DEG": "degrees",
    "MAG": "magnetic",
    "ELEV": "elevation",
    "ALT": "altitude",
    "MSL": "mean sea level",
    "AMSL": "above mean sea level",
    "AGL": "above ground level",
    "SFC": "surface",
    "GND": "ground",
    # misc
    "PSN": "position",
    "REF": "reference",
    "NR": "number",
    "INFO": "information",
    "CTC": "contact",
    "FREQ": "frequency",
    "MHZ": "megahertz",
    "KHZ": "kilohertz",
    "TEL": "telephone",
    "OBST": "obstacle",
    "HAZ": "hazard",
    "DUE": "due to",
    "WI": "within",
    "EXER": "exercise",
    "PJE": "parachute jumping exercise",
    "AERODROME": "aerodrome",
}

import re as _re

_TOKEN_RE = _re.compile(r"[A-Za-z0-9]+(?:/[A-Za-z0-9]+)*")


def expand(text: str) -> str:
    """Expand ICAO abbreviations in free text, token by token.

    Unknown tokens pass through unchanged, so invented or misspelled
    abbreviations are never silently rewritten.
    """
    def replace(match: "_re.Match[str]") -> str:
        token = match.group(0)
        plain = ABBREVIATIONS.get(token.upper())
        return plain if plain is not None else token

    return _TOKEN_RE.sub(replace, text)
