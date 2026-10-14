"""Tests for the NOTAM parser: header, items, Q line, times."""

import pytest
from datetime import datetime, timezone

from notam_decoder import NotamParseError, parse_notam

RWY_WIP = """(A1234/26 NOTAMN
Q) EGTT/QMRHW/IV/NBO/A/000/999/5129N00028W005
A) EGLL
B) 2610120900
C) 2610151700 EST
E) RWY 09R/27L CLSD DUE WIP. NO APCH LGT AVBL RWY 09R)"""


def test_header_fields():
    n = parse_notam(RWY_WIP)
    assert (n.series, n.number, n.year, n.kind) == ("A", 1234, 26, "N")
    assert n.replaces is None


def test_replacement_header_references_old_notam():
    n = parse_notam(
        "(B0007/26 NOTAMR B0001/26\n"
        "Q) VGFR/QFAXX/IV/NBO/A/000/999/2339N09024E005\n"
        "A) VGHS B) 2610010000 C) PERM E) AD OPR)"
    )
    assert n.kind == "R"
    assert n.replaces == "B0001/26"


def test_cancellation_header():
    n = parse_notam(
        "C0099/26 NOTAMC C0090/26 "
        "Q) EGTT/QXXXX/IV/NBO/A/000/999/5129N00028W005 "
        "A) EGLL B) 2610100800 C) 2610100900 E) CNL"
    )
    assert n.kind == "C"
    assert n.replaces == "C0090/26"


def test_q_line_fields():
    q = parse_notam(RWY_WIP).qualifier
    assert q.fir == "EGTT"
    assert q.qcode == "QMRHW"
    assert q.qcode_subject == "runway"
    assert q.qcode_condition == "work in progress"
    assert q.traffic == "IV"
    assert q.traffic_decoded == "IFR and VFR traffic"
    assert q.scope == "A"
    assert q.scope_decoded == "aerodrome"


def test_q_line_purpose_letters_decoded_individually():
    q = parse_notam(RWY_WIP).qualifier
    assert q.purpose == "NBO"
    assert "immediate attention" in q.purpose_decoded[0]
    assert "pre-flight information bulletins" in q.purpose_decoded[1]
    assert len(q.purpose_decoded) == 3


def test_q_line_coordinates_to_decimal_degrees():
    q = parse_notam(RWY_WIP).qualifier
    assert q.lat == pytest.approx(51 + 29 / 60, abs=1e-6)
    assert q.lon == pytest.approx(-(0 + 28 / 60), abs=1e-6)
    assert q.radius_nm == 5


def test_southern_western_hemisphere_signs():
    text = (
        "A0001/26 NOTAMN "
        "Q) SBBS/QWUXX/IV/M/W/000/010/2330S04638W010 "
        "A) SBGR B) 2610010000 C) 2610020000 E) UAS OPR"
    )
    q = parse_notam(text).qualifier
    assert q.lat == pytest.approx(-(23 + 30 / 60), abs=1e-6)
    assert q.lon == pytest.approx(-(46 + 38 / 60), abs=1e-6)
    assert q.qcode_subject == "unmanned aircraft"


def test_unknown_qcode_does_not_raise():
    text = (
        "A0002/26 NOTAMN "
        "Q) EGTT/QZZZZ/IV/NBO/A/000/999/5129N00028W005 "
        "A) EGLL B) 2610010000 C) 2610020000 E) SOMETHING ODD"
    )
    q = parse_notam(text).qualifier
    assert q.qcode_subject is None
    assert q.qcode_condition is None


def test_bad_qcode_field_count_rejected():
    with pytest.raises(NotamParseError):
        parse_notam(
            "A0003/26 NOTAMN Q) EGTT/QMRXX/IV A) EGLL "
            "B) 2610010000 C) 2610020000 E) X"
        )


def test_validity_times_and_estimated_flag():
    n = parse_notam(RWY_WIP)
    assert n.valid_from == datetime(2026, 10, 12, 9, 0, tzinfo=timezone.utc)
    assert n.valid_to == datetime(2026, 10, 15, 17, 0, tzinfo=timezone.utc)
    assert n.end_estimated is True
    assert n.permanent is False


def test_perm_end_gives_none_valid_to():
    n = parse_notam(
        "A0004/26 NOTAMN Q) EGTT/QFAXX/IV/NBO/A/000/999/5129N00028W005 "
        "A) EGLL B) 2610010000 C) PERM E) AD OPR"
    )
    assert n.permanent is True
    assert n.valid_to is None


def test_bad_time_group_rejected():
    with pytest.raises(NotamParseError):
        parse_notam(
            "A0005/26 NOTAMN Q) EGTT/QFAXX/IV/NBO/A/000/999/5129N00028W005 "
            "A) EGLL B) 2613320000 C) 2610020000 E) X"
        )


def test_missing_q_line_rejected():
    with pytest.raises(NotamParseError):
        parse_notam("A0006/26 NOTAMN A) EGLL B) 2610010000 E) X")


def test_not_a_notam_rejected():
    with pytest.raises(NotamParseError):
        parse_notam("hello world, this is not a notam")


def test_multiple_locations_kept():
    n = parse_notam(
        "A0007/26 NOTAMN Q) LOVV/QWPLW/IV/BO/W/000/130/4809N01610E001 "
        "A) LOWW LOWI B) 2610010000 C) 2610020000 E) PJE"
    )
    assert n.locations == ("LOWW", "LOWI")


def test_single_line_without_parens():
    n = parse_notam(RWY_WIP.strip()[1:-1].replace("\n", " "))
    assert n.series == "A" and n.number == 1234


def test_raw_preserved_verbatim():
    assert parse_notam(RWY_WIP).raw == RWY_WIP
