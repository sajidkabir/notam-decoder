"""Command line interface for notam-decoder."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone

from .parser import NotamParseError, parse_notam
from .summary import decoded_text, plain_summary


def _notam_to_json(notam) -> dict:
    data = asdict(notam)
    for key in ("valid_from", "valid_to"):
        value = data[key]
        data[key] = value.isoformat() if isinstance(value, datetime) else None
    data["purpose_decoded"] = list(data["qualifier"]["purpose_decoded"])
    data["locations"] = list(data["locations"])
    return data


def _read_input(path: str | None) -> str:
    if path is None or path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="notam-decode",
        description="Decode ICAO NOTAMs into structured data and plain English.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="file containing the NOTAM (default: stdin)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "summary"),
        default="text",
        help="output style (default: text)",
    )
    args = parser.parse_args(argv)

    try:
        text = _read_input(args.path)
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
        return 2
    try:
        notam = parse_notam(text)
    except NotamParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(_notam_to_json(notam), indent=2))
    elif args.format == "summary":
        print(plain_summary(notam))
    else:
        print(decoded_text(notam))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
