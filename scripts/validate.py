#!/usr/bin/env python3
"""Simple YAML validator for data/restaurants.yaml."""

import argparse
import datetime as dt
import re
import sys

try:
    import yaml  # type: ignore
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write("Missing dependency: install with `pip install -r scripts/requirements.txt`\n")
    raise exc

PRICE_VALUES = {"$", "$$", "$$$"}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
ORDERING_VALUES = {"dine-in", "takeout", "delivery"}
DIETARY_KEYS = ["vegetarian_friendly", "vegan_options", "gluten_free_friendly"]
HOUR_PATTERN = re.compile(r"^(closed|\d{1,2}:\d{2}-\d{1,2}:\d{2})$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_entry(entry, idx, errors):
    prefix = f"entry[{idx}] ({entry.get('name', 'unnamed')})"
    required_fields = [
        "name",
        "town",
        "address",
        "phone",
        "website",
        "cuisine",
        "price",
        "ordering",
        "dietary",
        "hours",
        "highlight_items",
        "notes",
        "last_verified",
        "sources",
    ]

    for field in required_fields:
        if field not in entry:
            errors.append(f"{prefix}: missing field `{field}`")

    if "price" in entry and entry["price"] not in PRICE_VALUES:
        errors.append(f"{prefix}: price must be one of {sorted(PRICE_VALUES)}")

    if "ordering" in entry:
        ordering = entry.get("ordering", [])
        if not isinstance(ordering, list) or not ordering:
            errors.append(f"{prefix}: ordering must be a non-empty list")
        else:
            bad = [o for o in ordering if o not in ORDERING_VALUES]
            if bad:
                errors.append(f"{prefix}: invalid ordering values {bad}; allowed {sorted(ORDERING_VALUES)}")

    if "dietary" in entry:
        dietary = entry.get("dietary", {})
        if not isinstance(dietary, dict):
            errors.append(f"{prefix}: dietary must be a mapping")
        else:
            for key in DIETARY_KEYS:
                if key not in dietary:
                    errors.append(f"{prefix}: dietary missing `{key}`")
                elif not isinstance(dietary[key], bool):
                    errors.append(f"{prefix}: dietary `{key}` must be boolean")

    if "hours" in entry:
        hours = entry.get("hours", {})
        if not isinstance(hours, dict):
            errors.append(f"{prefix}: hours must be a mapping")
        else:
            for day in DAYS:
                if day not in hours:
                    errors.append(f"{prefix}: hours missing `{day}`")
                else:
                    value = str(hours[day])
                    if not HOUR_PATTERN.match(value):
                        errors.append(f"{prefix}: hours for `{day}` must match HH:MM-HH:MM or `closed` (got `{value}`)")

    if "highlight_items" in entry:
        items = entry.get("highlight_items", [])
        if not isinstance(items, list):
            errors.append(f"{prefix}: highlight_items must be a list")
        else:
            for item in items:
                if not isinstance(item, dict):
                    errors.append(f"{prefix}: highlight_items entries must be mappings")
                    continue
                if "item" not in item or "note" not in item:
                    errors.append(f"{prefix}: highlight_items entries must include `item` and `note`")

    if "last_verified" in entry:
        lv = str(entry.get("last_verified"))
        if not DATE_PATTERN.match(lv):
            errors.append(f"{prefix}: last_verified must be YYYY-MM-DD (got `{lv}`)")
        else:
            try:
                dt.date.fromisoformat(lv)
            except ValueError:
                errors.append(f"{prefix}: last_verified is not a valid date ({lv})")

    if "sources" in entry:
        sources = entry.get("sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}: sources must be a non-empty list")
        else:
            for s in sources:
                if not isinstance(s, dict):
                    errors.append(f"{prefix}: each source must be a mapping with `type` and `detail`")
                    continue
                if "type" not in s or "detail" not in s:
                    errors.append(f"{prefix}: each source needs `type` and `detail`")

    if "comments" in entry:
        comments = entry.get("comments", [])
        if not isinstance(comments, list):
            errors.append(f"{prefix}: comments must be a list of strings")
        else:
            for c in comments:
                if not isinstance(c, str):
                    errors.append(f"{prefix}: each comment must be a string")


def main():
    parser = argparse.ArgumentParser(description="Validate restaurant YAML data.")
    parser.add_argument("path", nargs="?", default="data/restaurants.yaml", help="Path to YAML file")
    args = parser.parse_args()

    data = load_yaml(args.path)
    errors = []

    if not isinstance(data, list):
        sys.stderr.write("Top-level YAML must be a list of restaurant entries\n")
        sys.exit(1)

    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"entry[{idx}]: must be a mapping")
            continue
        validate_entry(entry, idx, errors)

    if errors:
        for err in errors:
            print(err)
        sys.exit(1)

    print(f"OK: {len(data)} entries validated")


if __name__ == "__main__":
    main()
