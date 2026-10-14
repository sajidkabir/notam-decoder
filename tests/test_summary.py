"""Tests for plain language summary and decoded text rendering."""

from notam_decoder import parse_notam
from notam_decoder.summary import decoded_text, plain_summary

WIP = """(A1234/26 NOTAMN
Q) EGTT/QMRHW/IV/NBO/A/000/999/5129N00028W005
A) EGLL
B) 2610120900
C) 2610151700 EST
E) RWY 09R/27L CLSD DUE WIP)"""


def test_summary_names_notam_subject_and_condition():
    summary = plain_summary(parse_notam(WIP))
    assert "NOTAM A1234/26" in summary
    assert "Runway: work in progress" in summary
    assert "EGLL" in summary


def test_summary_states_validity_window_and_estimated_end():
    summary = plain_summary(parse_notam(WIP))
    assert "12 Oct 2026 09:00 UTC" in summary
    assert "15 Oct 2026 17:00 UTC" in summary
    assert "estimated end" in summary


def test_summary_includes_expanded_detail_text():
    summary = plain_summary(parse_notam(WIP))
    assert "runway 09R/27L closed due to work in progress" in summary


def test_summary_flags_unknown_qcode_honestly():
    text = (
        "A0002/26 NOTAMN "
        "Q) EGTT/QZZZZ/IV/NBO/A/000/999/5129N00028W005 "
        "A) EGLL B) 2610010000 C) 2610020000 E) SOMETHING ODD"
    )
    summary = plain_summary(parse_notam(text))
    assert "not in this decoder's tables" in summary


def test_summary_perm_end():
    text = (
        "A0004/26 NOTAMN Q) EGTT/QFAXX/IV/NBO/A/000/999/5129N00028W005 "
        "A) EGLL B) 2610010000 C) PERM E) AD OPR"
    )
    assert "until further notice (permanent)" in plain_summary(parse_notam(text))


def test_summary_includes_schedule_and_limits():
    text = (
        "(B0422/26 NOTAMN "
        "Q) VGFR/QRDCA/IV/BO/W/000/045/2339N09024E010 "
        "A) VGHS B) 2610150200 C) 2610160600 "
        "D) DAILY SR-SS "
        "E) TEMPO DANGER AREA ACT "
        "F) SFC G) 4500FT AMSL)"
    )
    summary = plain_summary(parse_notam(text))
    assert "daily sunrise to sunset" in summary
    assert "surface to 4500 feet above mean sea level" in summary


def test_summary_mentions_replaced_notam():
    text = (
        "(B0007/26 NOTAMR B0001/26 "
        "Q) VGFR/QFAXX/IV/NBO/A/000/999/2339N09024E005 "
        "A) VGHS B) 2610010000 C) PERM E) AD OPR)"
    )
    assert "replaces B0001/26" in plain_summary(parse_notam(text))


def test_decoded_text_renders_all_items():
    out = decoded_text(parse_notam(WIP))
    assert "A1234/26 NOTAMN" in out
    assert "subject: runway" in out
    assert "condition: work in progress" in out
    assert "traffic: IFR and VFR traffic" in out
    assert "scope: aerodrome" in out
    assert "area centre: 51.483333" in out
    assert "A) EGLL" in out
    assert "B) 12 Oct 2026 09:00 UTC" in out
    assert "(estimated)" in out
    assert "runway 09R/27L closed due to work in progress" in out
