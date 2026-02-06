#!/usr/bin/env python3
"""
Test that report.md Liquid variables resolve correctly from report_stats.json.

Run after `python notebooks/analysis.py` to verify the report would render
with the correct stats. No Jekyll required.

Usage:
  python scripts/test_report_render.py
  # or from repo root:
  python -m scripts.test_report_render
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT / "docs" / "report.md"
DATA_PATH = ROOT / "docs" / "_data" / "report_stats.json"


def get_nested(data: dict, path: list):
    """Get value from nested dict by path, e.g. ['nc', 'Sr', 'count']."""
    for key in path:
        data = data[key]
    return data


def render_report_stats(content: str, data: dict) -> str:
    """Replace {{ site.data.report_stats.xxx.yyy.zzz }} with values from data."""
    pattern = re.compile(r"\{\{\s*site\.data\.report_stats\.([A-Za-z0-9_.]+)\s*\}\}")
    rendered = content

    for m in pattern.finditer(content):
        full_placeholder = m.group(0)
        path_str = m.group(1)
        path = path_str.split(".")
        try:
            value = get_nested(data, path)
            rendered = rendered.replace(full_placeholder, str(value), 1)
        except (KeyError, TypeError) as e:
            raise AssertionError(f"Cannot resolve {{ site.data.report_stats.{path_str} }}: {e}")

    return rendered


def main():
    assert DATA_PATH.exists(), f"Run analysis first: {DATA_PATH} not found"
    assert REPORT_PATH.exists(), f"Report missing: {REPORT_PATH}"

    data = json.loads(DATA_PATH.read_text())
    content = REPORT_PATH.read_text()

    rendered = render_report_stats(content, data)

    # All report_stats placeholders should be replaced
    unreplaced = re.findall(r"\{\{\s*site\.data\.report_stats\.[^}]+\}\}", rendered)
    assert not unreplaced, f"Unreplaced placeholders: {unreplaced}"

    # Sanity: rendered report should contain key numbers from data
    nc_sr = data["nc"]["Sr"]
    aa_sr = data["aa"]["Sr"]
    assert str(nc_sr["count"]) in rendered, "NC Sr count should appear in rendered report"
    assert nc_sr["pct"] in rendered, "NC Sr pct should appear in rendered report"
    assert str(aa_sr["count"]) in rendered, "AA Sr count should appear in rendered report"
    assert aa_sr["pct"] in rendered, "AA Sr pct should appear in rendered report"

    print("OK: All report_stats placeholders resolve; rendered report contains expected values.")


if __name__ == "__main__":
    main()
