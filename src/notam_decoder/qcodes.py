"""ICAO NOTAM Q-code tables.

The Q-code is the five letter group in the Q) line. Letter 1 is always Q.
Letters 2 and 3 name the subject; letters 4 and 5 name the condition.
These meanings follow ICAO Doc 8126 / Annex 15. The tables cover the
subjects and conditions seen most often in the field; anything missing
decodes to None so the caller can fall back to the item E text instead
of guessing.
"""

SUBJECTS: dict[str, str] = {
    # F: AGA facilities
    "FA": "aerodrome",
    "FB": "braking action measurement equipment",
    "FC": "friction measuring device",
    "FD": "docking system",
    "FF": "fire fighting and rescue",
    "FG": "ground movement control",
    "FH": "helicopter alighting area/platform",
    "FI": "aircraft de-icing facilities",
    "FJ": "fuel and oil",
    "FL": "landing direction indicator",
    "FM": "meteorological service",
    "FO": "fog dispersal system",
    "FP": "heliport",
    "FS": "snow removal equipment",
    "FT": "transmissometer",
    "FU": "fuel availability",
    "FZ": "customs/immigration",
    # L: lighting facilities
    "LA": "approach lighting system",
    "LB": "aerodrome beacon",
    "LC": "runway centre line lights",
    "LD": "landing direction indicator lights",
    "LE": "runway edge lights",
    "LF": "sequenced flashing lights",
    "LG": "temporary obstruction lights",
    "LH": "high intensity runway lights",
    "LI": "runway end identifier lights",
    "LJ": "runway alignment indicator lights",
    "LL": "low intensity runway lights",
    "LM": "medium intensity runway lights",
    "LP": "PAPI",
    "LR": "all landing area lighting facilities",
    "LS": "stopway lights",
    "LT": "threshold lights",
    "LU": "helicopter approach path indicator",
    "LV": "visual approach slope indicator system",
    "LW": "heliport lighting",
    "LX": "taxiway centre line lights",
    "LY": "taxiway edge lights",
    "LZ": "runway touchdown zone lights",
    # M: movement and landing area
    "MA": "movement area",
    "MB": "bearing strength",
    "MC": "clearway",
    "MD": "declared distances",
    "MG": "taxiing guidance system",
    "MH": "runway arresting gear",
    "MK": "parking area",
    "MM": "daylight markings",
    "MN": "apron",
    "MO": "stopbar",
    "MP": "aircraft stands",
    "MR": "runway",
    "MS": "stopway",
    "MT": "threshold",
    "MU": "runway turning bay",
    "MW": "strip/shoulder",
    "MX": "taxiway",
    # O: obstacles
    "OA": "aeronautical ground light",
    "OB": "obstacle",
    "OE": "aircraft entry requirements",
    "OL": "obstacle limitation surfaces",
    # I: instrument landing system
    "IA": "instrument landing system",
    "IG": "glide path",
    "IL": "localizer",
    "IM": "inner marker",
    "IO": "outer marker",
    # N: radio navigation aids
    "NA": "all radio navigation facilities",
    "NB": "non-directional radio beacon",
    "NC": "DECCA",
    "ND": "distance measuring equipment",
    "NF": "fan marker",
    "NL": "locator",
    "NM": "VOR/DME",
    "NN": "TACAN",
    "NT": "VORTAC",
    "NV": "VOR",
    "NX": "direction-finding station",
    # C: communications
    "CA": "air/ground facility",
    "CE": "en-route facility",
    "CG": "ground controlled approach system",
    "CS": "ATIS",  # automatic terminal information service
    # R: ATS airspace organization
    "RA": "airspace reservation",
    "RD": "danger area",
    "RO": "overflying",
    "RP": "prohibited area",
    # S: ATS routes
    "SA": "ATS route",
    # P: air traffic procedures
    "PF": "air traffic flow management",
    "PH": "holding procedure",
    "PX": "minimum holding altitude",
    # W: warnings
    "WA": "air display",
    "WB": "aerobatics",
    "WC": "captive balloon or kite",
    "WD": "demolition of explosives",
    "WE": "military exercises",
    "WF": "aerial refuelling",
    "WG": "glider flying",
    "WJ": "banner/target towing",
    "WM": "missile, gun or rocket firing",
    "WP": "parachute jumping exercise",
    "WR": "radioactive materials or toxic chemicals",
    "WS": "burning or blowing gas",
    "WT": "mass movement of aircraft",
    "WU": "unmanned aircraft",
    "WV": "formation flight",
    "WW": "significant volcanic activity",
    "WY": "aerial survey",
    "WZ": "model flying",
}

CONDITIONS: dict[str, str] = {
    "AC": "withdrawn for maintenance",
    "AD": "available for daylight operation",
    "AF": "flight checked and found reliable",
    "AG": "operating but ground checked only, awaiting flight check",
    "AH": "hours of service are now",
    "AK": "resumed normal operation",
    "AL": "operative",
    "AM": "military operations only",
    "AN": "available for night operation",
    "AO": "operational",
    "AP": "available, prior permission required",
    "AR": "available on request",
    "AS": "unserviceable",
    "AU": "not available",
    "AW": "withdrawn",
    "AX": "previously promulgated shutdown has been cancelled",
    "CA": "activated",
    "CC": "completed",
    "CD": "deactivated",
    "CE": "erected",
    "CF": "operating frequency changed",
    "CG": "downgraded",
    "CH": "changed",
    "CI": "identification or radio call sign changed",
    "CL": "realigned",
    "CM": "displaced",
    "CN": "cancelled",
    "CO": "operating",
    "CR": "temporarily replaced",
    "CS": "installed",
    "CT": "on test, do not use",
    "HA": "braking action is",
    "HB": "friction coefficient is",
    "HC": "covered by compacted snow to a depth of",
    "HD": "covered by dry snow to a depth of",
    "HE": "covered by water to a depth of",
    "HF": "totally free of snow and ice",
    "HG": "grass cutting in progress",
    "HH": "hazard due to",
    "HI": "covered by ice",
    "HJ": "launch planned",
    "HK": "bird migration in progress",
    "HL": "snow clearance completed",
    "HM": "marked by",
    "HN": "covered by wet snow or slush to a depth of",
    "HO": "obscured by snow",
    "HP": "snow clearance in progress",
    "HQ": "operation cancelled",
    "HR": "standing water",
    "HS": "sanding in progress",
    "HT": "approach according to signal area only",
    "HU": "launch in progress",
    "HV": "work completed",
    "HW": "work in progress",
    "HX": "concentration of birds",
    "HY": "snow banks exist",
    "HZ": "covered by frozen ruts and ridges",
    "LA": "operating on auxiliary power supply",
    "LB": "reserved for aircraft based therein",
    "LC": "closed",
    "LD": "unsafe",
    "LE": "operating without auxiliary power supply",
    "LF": "interference from",
    "LG": "operating without identification",
    "LH": "unserviceable for aircraft heavier than",
    "LI": "closed to all night operations",
    "LK": "operating as a fixed light",
    "LL": "usable for stated length and width",
    "LP": "prohibited",
    "LR": "aircraft restricted to runways and taxiways",
    "LS": "subject to interruption",
    "LT": "limited",
    "LV": "closed",
    "LW": "will take place",
    "LX": "operating but caution advised",
    "XX": "plain language following",
}

TRAFFIC: dict[str, str] = {
    "I": "IFR traffic",
    "V": "VFR traffic",
    "IV": "IFR and VFR traffic",
    "K": "checklist",
}

PURPOSE: dict[str, str] = {
    "N": "for the immediate attention of aircraft operators",
    "B": "for pre-flight information bulletins",
    "O": "operationally significant for IFR flights",
    "M": "miscellaneous",
    "K": "checklist",
}

SCOPE: dict[str, str] = {
    "A": "aerodrome",
    "E": "en-route",
    "W": "navigation warning",
    "K": "checklist",
}


def decode_subject(code: str) -> str | None:
    """Plain words for Q-code letters 2-3, or None when unknown."""
    if len(code) != 5 or not code.startswith("Q"):
        return None
    return SUBJECTS.get(code[1:3].upper())


def decode_condition(code: str) -> str | None:
    """Plain words for Q-code letters 4-5, or None when unknown."""
    if len(code) != 5 or not code.startswith("Q"):
        return None
    return CONDITIONS.get(code[3:5].upper())


def decode_traffic(value: str) -> str | None:
    return TRAFFIC.get(value.upper())


def decode_purpose(value: str) -> tuple[str, ...]:
    """One decoded phrase per purpose letter, skipping unknown letters."""
    return tuple(PURPOSE[ch] for ch in value.upper() if ch in PURPOSE)


def decode_scope(value: str) -> str | None:
    return SCOPE.get(value.upper())
