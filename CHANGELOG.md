# Changelog

All notable changes to this project are recorded here. Versions follow
semantic versioning.

## [0.1.0] - 2026-10-12

Initial release.

### Added

- ICAO NOTAM parser: header (series, number, year, NOTAMN/NOTAMR/NOTAMC
  with replaced/cancelled reference), Q) qualifier line, items A to G.
- Q-code decoding: subject (letters 2-3) and condition (letters 4-5) in
  plain words per ICAO Doc 8126; traffic (I/V/IV), purpose (N/B/O/M),
  scope (A/E/W); Q-line coordinates converted to decimal degrees and
  radius in nautical miles.
- UTC datetime parsing for B) and C), with PERM and EST handled.
- Item D schedule decoding: day ranges, clock times, DAILY, EXC, SR-SS,
  H24, FM/TIL/BTN.
- Item E ICAO abbreviation expansion (Doc 8400 based), token by token;
  unknown tokens pass through unchanged.
- Item F/G height limit decoding: SFC, GND, FLnnn, nnnnFT, AMSL/AGL.
- Plain language summary and multi-line decoded text renderers.
- `notam-decode` CLI: text, json, and summary output styles; file or
  stdin input.
- 47 pytest checks; three example NOTAMs plus a demo script.
