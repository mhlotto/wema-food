# Data schema and style

- One YAML file per restaurant under `data/restaurants/` (filenames kebab-case, e.g., `pita-pockets.yaml`).
- Keep entries alphabetized by `name`.
- Strings in quotes only when they contain punctuation; phone numbers as `413-555-0100`.
- `price`: `$`, `$$`, or `$$$` (rough guide, not exact).
- `hours`: use 24h ranges like `11:00-21:00`; use `closed` if not open that day.
- `categories`: optional tags like `restaurant`, `bar`, `cafe` (can include more than one).
- `ordering`: any of `dine-in`, `takeout`, `delivery`.
- `offerings`: optional list from `food`, `alcohol`, `coffee` to power “open for drinks/coffee/food” filters.
- `dietary`: booleans; default to `false` if unknown.
- `highlight_items`: keep to 1-3 items with short notes.
- `sources`: cite how you know (visit date, menu URL, Instagram update).
- After edits, run `python scripts/build_data.py` to regenerate `data/restaurants.yaml` and `docs/restaurants.yaml`.

## Field reference
- `name`: Restaurant name.
- `town`: e.g., Amherst, Hadley.
- `neighborhood`: Optional detail (e.g., Downtown Amherst, North Amherst).
- `address`: Street, city, state.
- `coordinates`: Optional, `lat` and `lng` decimals.
- `phone`, `website`: Contact info.
- `cuisine`: Short description (e.g., "Middle Eastern", "Thai", "Coffee").
- `price`: `$`/`$$`/`$$$`.
- `categories`: Optional list of tags such as `restaurant`, `bar`, `cafe`.
- `ordering`: List of service modes.
- `offerings`: Optional list of service types (`food`, `alcohol`, `coffee`).
- `dietary`: `vegetarian_friendly`, `vegan_options`, `gluten_free_friendly`.
- `hours`: Map of day -> time window string.
- `highlight_items`: List of signature dishes with `item` and `note`.
- `notes`: Freeform quick facts (parking, cash-only, wait times, seasonal).
- `comments`: Optional list of short freeform notes (e.g., user observations, seasonal specials).
- `last_verified`: Date you confirmed the info.
- `sources`: List of `{ type, detail }` entries.
