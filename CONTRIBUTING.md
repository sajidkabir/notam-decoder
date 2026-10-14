# Contributing

Contributions are welcome: bug reports, decoding corrections, new Q-code
subjects or conditions, new ICAO abbreviations, documentation, and
examples. This project aims to stay small, readable, dependency free,
and honest about what it does not yet decode.

## Getting set up

```bash
git clone https://github.com/sajidkabir/notam-decoder.git
cd notam-decoder
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
pytest -q
```

All tests should pass before you change anything. The package is pure
standard library, so there is nothing else to install.

## Making a change

1. Fork the repository and create a branch from `main`
   (`git checkout -b feature/short-name`).
2. Keep the change focused. One code group, one abbreviation set, one
   fix, or one feature per pull request.
3. Add or update tests. Decoding changes need a check against a real or
   realistic NOTAM, and the test should say which field of which NOTAM
   pins the behavior down.
4. Run `pytest -q` and make sure it is green.

## Decoding corrections

Q-code and abbreviation meanings follow ICAO Doc 8126 and Doc 8400. If
a code decodes wrong, open an issue with the NOTAM text (or a realistic
redacted version) and the expected meaning, and cite the ICAO reference
where possible. Unknown codes should stay unknown rather than be
guessed; that honesty is a feature.
