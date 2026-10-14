"""Plain language rendering of a parsed NOTAM."""

from __future__ import annotations

from datetime import datetime

from .models import Notam

_KIND = {"N": "new", "R": "replacement", "C": "cancellation"}


def _stamp(dt: datetime) -> str:
    return dt.strftime("%-d %b %Y %H:%M UTC")


def plain_summary(notam: Notam) -> str:
    """One paragraph plain English summary of the NOTAM."""
    q = notam.qualifier
    parts = [f"NOTAM {notam.series}{notam.number:04d}/{notam.year:02d}"]

    kind = _KIND.get(notam.kind, notam.kind)
    parts.append(f"({kind} NOTAM)")
    if notam.replaces:
        verb = "replaces" if notam.kind == "R" else "cancels"
        parts.append(f"{verb} {notam.replaces}.")

    subject = q.qcode_subject
    condition = q.qcode_condition
    if subject and condition:
        what = f"{subject}: {condition}"
    elif subject:
        what = subject
    elif q.qcode:
        what = f"NOTAM code {q.qcode} (not in this decoder's tables, see text below)"
    else:
        what = "see text below"
    parts.append(f"{what[0].upper()}{what[1:]}.")

    parts.append(f"Location: {', '.join(notam.locations)}.")

    window = f"Valid from {_stamp(notam.valid_from)}"
    if notam.permanent:
        window += " until further notice (permanent)."
    elif notam.valid_to is not None:
        window += f" to {_stamp(notam.valid_to)}"
        window += " (estimated end)" if notam.end_estimated else "."
    parts.append(window)

    if notam.schedule_decoded:
        parts.append(f"Active: {notam.schedule_decoded}.")
    if notam.lower_limit_decoded and notam.upper_limit_decoded:
        parts.append(
            f"Height limits: {notam.lower_limit_decoded} to "
            f"{notam.upper_limit_decoded}."
        )
    parts.append(f"Detail: {notam.text_decoded}")
    return " ".join(parts)


def decoded_text(notam: Notam) -> str:
    """Multi-line decode: qualifier, items, and expanded text."""
    q = notam.qualifier
    lines = [
        f"{notam.series}{notam.number:04d}/{notam.year:02d} "
        f"NOTAM{notam.kind}"
        + (f" (replaces/cancels {notam.replaces})" if notam.replaces else ""),
        f"Q) FIR {q.fir}, code {q.qcode}",
    ]
    if q.qcode_subject:
        lines.append(f"   subject: {q.qcode_subject}")
    if q.qcode_condition:
        lines.append(f"   condition: {q.qcode_condition}")
    lines.append(f"   traffic: {q.traffic_decoded}")
    lines.append(f"   purpose: {'; '.join(q.purpose_decoded)}")
    lines.append(f"   scope: {q.scope_decoded}")
    if q.lat is not None and q.lon is not None:
        lines.append(
            f"   area centre: {q.lat}, {q.lon}"
            + (f", radius {q.radius_nm} NM" if q.radius_nm else "")
        )
    lines.append(f"A) {', '.join(notam.locations)}")
    lines.append(f"B) {_stamp(notam.valid_from)}")
    if notam.permanent:
        lines.append("C) permanent")
    elif notam.valid_to is not None:
        est = " (estimated)" if notam.end_estimated else ""
        lines.append(f"C) {_stamp(notam.valid_to)}{est}")
    if notam.schedule_decoded:
        lines.append(f"D) {notam.schedule_decoded}")
    lines.append(f"E) {notam.text_decoded}")
    if notam.lower_limit_decoded:
        lines.append(f"F) {notam.lower_limit_decoded}")
    if notam.upper_limit_decoded:
        lines.append(f"G) {notam.upper_limit_decoded}")
    return "\n".join(lines)
