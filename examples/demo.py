"""Demonstrate the notam-decoder API on the bundled example NOTAMs."""

from pathlib import Path

from notam_decoder import parse_notam, plain_summary, decoded_text

EXAMPLES = Path(__file__).with_suffix("").parent

for name in ("runway_wip.notam", "parachute.notam", "unmanned.notam"):
    path = EXAMPLES / name
    notam = parse_notam(path.read_text(encoding="utf-8"))
    print("=" * 72)
    print(name)
    print("=" * 72)
    print(decoded_text(notam))
    print()
    print(plain_summary(notam))
    print()
