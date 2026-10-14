"""Tests for the notam-decode command line interface."""

import json
import subprocess
import sys
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
WIP = EXAMPLES / "runway_wip.notam"


def run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "notam_decoder.cli", *args],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=EXAMPLES.parent,
    )


def test_cli_text_output(tmp_path):
    result = run_cli(str(WIP))
    assert result.returncode == 0, result.stderr
    assert "A1234/26 NOTAMN" in result.stdout
    assert "subject: runway" in result.stdout


def test_cli_json_output_is_parseable():
    result = run_cli(str(WIP), "--format", "json")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["series"] == "A" and data["number"] == 1234
    assert data["qualifier"]["qcode_subject"] == "runway"
    assert data["valid_from"].startswith("2026-10-12")


def test_cli_summary_output():
    result = run_cli(str(WIP), "--format", "summary")
    assert result.returncode == 0, result.stderr
    assert "Runway: work in progress" in result.stdout


def test_cli_reads_stdin():
    result = run_cli(stdin=WIP.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert "A1234/26 NOTAMN" in result.stdout


def test_cli_bad_input_exits_2():
    result = run_cli(stdin="not a notam at all")
    assert result.returncode == 2
    assert "error" in result.stderr.lower()


def test_cli_missing_file_exits_2():
    result = run_cli("/nonexistent/file.notam")
    assert result.returncode == 2
