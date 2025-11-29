#!/usr/bin/env python3
"""
Aggregate per-restaurant YAML files into data/restaurants.yaml and docs/restaurants.yaml.
"""

import glob
import os
from pathlib import Path
from typing import List

import yaml  # type: ignore
from html import escape


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "data" / "restaurants"
AGG_PATH = ROOT / "data" / "restaurants.yaml"
DOCS_PATH = ROOT / "docs" / "restaurants.yaml"
INDEX_PATH = ROOT / "docs" / "index.html"


def load_entries() -> List[dict]:
    entries = []
    for path in sorted(glob.glob(str(SRC_DIR / "*.yaml"))):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, list):
                entries.extend(data)
            elif isinstance(data, dict):
                entries.append(data)
            else:
                raise ValueError(f"{path} must contain a mapping or list of mappings")
    entries.sort(key=lambda e: e.get("name", "").lower())
    return entries


def write_yaml(path: Path, data: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=False)
    print(f"Wrote {len(data)} entries to {path}")


def main() -> None:
    if not SRC_DIR.exists():
        raise SystemExit(f"Source folder not found: {SRC_DIR}")
    entries = load_entries()
    write_yaml(AGG_PATH, entries)
    if DOCS_PATH.parent.exists():
        write_yaml(DOCS_PATH, entries)
    else:
        print("docs/ folder not found; skipped writing docs/restaurants.yaml")
    update_static_fallback(entries)


def update_static_fallback(entries: list) -> None:
    """Render a lightweight static table into docs/index.html between marker comments."""
    if not INDEX_PATH.exists():
        print("docs/index.html not found; skipped static fallback injection")
        return
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- STATIC_FALLBACK_START -->"
    end_marker = "<!-- STATIC_FALLBACK_END -->"
    if start_marker not in content or end_marker not in content:
        print("Static fallback markers not found in docs/index.html; skipped injection")
        return

    rows = []
    for entry in entries:
        name = escape(str(entry.get("name", "")))
        town = escape(str(entry.get("town", "")))
        neighborhood = escape(str(entry.get("neighborhood", "")))
        categories = ", ".join(entry.get("categories", []) or [])
        cuisine = escape(str(entry.get("cuisine", "")))
        price = escape(str(entry.get("price", "")))
        rows.append(
            f"<tr><td>{name}</td><td>{town}</td><td>{neighborhood}</td><td>{escape(categories)}</td><td>{cuisine}</td><td>{price}</td></tr>"
        )
    table_html = "\n".join(rows)

    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker)
    new_section = f"{start_marker}\n{table_html}\n{end_marker}"
    new_content = content[:start_idx] + new_section + content[end_idx + len(end_marker) :]

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated static fallback table in {INDEX_PATH}")


if __name__ == "__main__":
    main()
