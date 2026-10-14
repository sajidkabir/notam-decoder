"""Tests for Q-code, abbreviation, schedule, and level decoding."""

from notam_decoder import parse_notam
from notam_decoder.qcodes import (
    decode_condition,
    decode_purpose,
    decode_scope,
    decode_subject,
    decode_traffic,
)
from notam_decoder.abbreviations import expand
from notam_decoder.schedule import decode_level, decode_schedule


def test_subject_table_spot_checks():
    assert decode_subject("QMRXX") == "runway"
    assert decode_subject("QFALC") == "aerodrome"
    assert decode_subject("QWPLW") == "parachute jumping exercise"
    assert decode_subject("QWUHW") == "unmanned aircraft"
    assert decode_subject("QRDCA") == "danger area"
    assert decode_subject("QLCAS") == "runway centre line lights"


def test_condition_table_spot_checks():
    assert decode_condition("QFALC") == "closed"
    assert decode_condition("QMRHW") == "work in progress"
    assert decode_condition("QWPLW") == "will take place"
    assert decode_condition("QLCAS") == "unserviceable"
    assert decode_condition("QMRXX") == "plain language following"


def test_unknown_codes_return_none():
    assert decode_subject("QZZXX") is None
    assert decode_condition("QMRZZ") is None
    assert decode_subject("nope") is None


def test_traffic_scope_purpose():
    assert decode_traffic("IV") == "IFR and VFR traffic"
    assert decode_traffic("I") == "IFR traffic"
    assert decode_scope("W") == "navigation warning"
    assert decode_scope("E") == "en-route"
    assert decode_purpose("K") == ("checklist",)


def test_abbreviations_expand_whole_tokens():
    assert expand("RWY 09R/27L CLSD DUE WIP") == (
        "runway 09R/27L closed due to work in progress"
    )


def test_abbreviations_case_insensitive():
    assert expand("rwy clsd") == "runway closed"


def test_abbreviations_leave_unknown_tokens_alone():
    assert expand("FOOBAR RWY") == "FOOBAR runway"


def test_abbreviations_do_not_touch_embedded_tokens():
    assert expand("RUNWAY09") == "RUNWAY09"


def test_abbreviation_slash_token():
    assert expand("ILS U/S") == "instrument landing system unserviceable"


def test_schedule_day_range():
    assert decode_schedule("MON-FRI 0900-1700") == "Monday to Friday 09:00 to 17:00 UTC"
    assert decode_schedule("MON-FRI") == "Monday to Friday"
    assert decode_schedule("DAILY SR-SS") == "daily sunrise to sunset"
    assert decode_schedule("SAT SUN EXC") == "Saturday Sunday except"


def test_schedule_times_become_clock_times():
    assert decode_schedule("1100-1500") == "11:00 to 15:00 UTC"


def test_schedule_unknown_tokens_pass_through():
    assert decode_schedule("MON FOO") == "Monday FOO"


def test_level_sfc_fl_feet():
    assert decode_level("SFC") == "surface"
    assert decode_level("GND") == "ground"
    assert decode_level("FL130") == "flight level 130"
    assert decode_level("5000FT") == "5000 feet"


def test_level_datum_suffix():
    assert decode_level("4500FT AMSL") == "4500 feet above mean sea level"
    assert decode_level("1000FT AGL") == "1000 feet above ground level"


def test_level_unknown_passes_through():
    assert decode_level("SOMEWHERE") == "SOMEWHERE"


def test_item_d_and_fg_decoded_on_full_notam():
    text = (
        "(B0422/26 NOTAMN "
        "Q) VGFR/QRDCA/IV/BO/W/000/045/2339N09024E010 "
        "A) VGHS B) 2610150200 C) 2610160600 "
        "D) DAILY SR-SS "
        "E) TEMPO DANGER AREA ACT "
        "F) SFC G) 4500FT AMSL)"
    )
    n = parse_notam(text)
    assert n.schedule_decoded == "daily sunrise to sunset"
    assert n.lower_limit_decoded == "surface"
    assert n.upper_limit_decoded == "4500 feet above mean sea level"
    assert n.text_decoded == "temporarily danger area AREA ACT"
