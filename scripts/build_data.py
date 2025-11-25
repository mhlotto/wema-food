#!/usr/bin/env python3
"""
Aggregate per-restaurant YAML files into data/restaurants.yaml and docs/restaurants.yaml.
"""

import glob
import os
from pathlib import Path
from typing import List

import yaml  # type: ignore


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "data" / "restaurants"
AGG_PATH = ROOT / "data" / "restaurants.yaml"
DOCS_PATH = ROOT / "docs" / "restaurants.yaml"


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


if __name__ == "__main__":
    main()
