# 413 and Amherst, MA Area Food Guide

A community-maintained list of where to eat in and around Amherst, MA. Data lives in YAML, and friendly pages can be generated or browsed directly in GitHub. Pull requests are welcome for new spots, corrections, and guides.

**Live site:** https://mhlotto.github.io/413-food/docs/

## Repo map
- `data/restaurants/`: one YAML file per restaurant.
- `data/restaurants.yaml`: generated aggregate of all restaurants.
- `data/README.md`: schema and style notes.
- `guides/`: curated writeups (late-night, dietary needs, seasonal picks, etc.).
- `scripts/validate.py`: lint the data for required fields and formatting.
- `docs/index.html`: simple GitHub Pages view that reads the YAML and lists spots.

## Latest updates
- Last restaurant added: Pita Pockets (2024-10-15)
- Last comment added: “Takes a minute to cool; ask for extra hot sauce if you like heat.” (Pita Pockets)

## How to contribute
1) Pick your change type: add or edit a restaurant, or add a guide.
2) For restaurants: add a new file in `data/restaurants/` using the template below, fill the fields, and update `last_verified`. Required: `town`; optional but encouraged: `neighborhood`.
3) Keep notes concise and factual. Include a source (menu link or visit date) in `sources`.
4) For guides: add a new Markdown file under `guides/` using the guide template in `guides/README.md`.
5) Run `python scripts/build_data.py` to regenerate aggregated YAML (for validator and Pages).
6) Open a PR. If you spot mistakes, please also bump `last_verified` to the date you confirmed the info.

## Restaurant fields (summary)
- `name`, `neighborhood`, `address`, `phone`, `website`, optional `coordinates` (`lat`, `lng`).
- `cuisine`, `price` ($/$$/$$$), `ordering` (dine-in/takeout/delivery), `hours` (strings like `11:00-21:00`).
- `dietary` flags (vegetarian_friendly, vegan_options, gluten_free_friendly), `highlight_items` (signature dishes), `notes` (parking, cash-only, waits).
- Optional: `comments` (short freeform notes for the detail view).
- `last_verified` (YYYY-MM-DD) and `sources` (visited/menu/social links).

## Restaurant entry template
```yaml
- name: Example Restaurant
  town: Amherst
  neighborhood: Downtown
  address: 123 Main St, Amherst, MA
  coordinates:
    lat: 42.3750
    lng: -72.5190
  phone: 413-555-0100
  website: https://example.com
  cuisine: Example cuisine
  price: $$
  ordering:
    - dine-in
    - takeout
  dietary:
    vegetarian_friendly: true
    vegan_options: false
    gluten_free_friendly: false
  hours:
    mon: "11:00-21:00"
    tue: "11:00-21:00"
    wed: "11:00-21:00"
    thu: "11:00-21:00"
    fri: "11:00-22:00"
    sat: "11:00-22:00"
    sun: "12:00-20:00"
  highlight_items:
    - item: Signature dish
      note: Short note on why it is good
  notes: Quick facts (parking, cash-only, seasonal, long waits)
  comments:
    - Short freeform note
  last_verified: 2024-10-01
  sources:
    - type: visited
      detail: "Oct 2024"
    - type: menu
      detail: https://example.com/menu
```

## Guides
- Create a new Markdown file in `guides/` (e.g., `guides/late-night.md`).
- Use the template in `guides/README.md` (title, date, focus, and a small list of spots with links back to `data/restaurants.yaml`).

## Validate data
- Install tools: `pip install -r scripts/requirements.txt`.
- Aggregate and validate:
  - `python scripts/build_data.py` (combines `data/restaurants/*.yaml` into `data/restaurants.yaml` and `docs/restaurants.yaml`)
  - `python scripts/validate.py data/restaurants.yaml`
- The script checks required fields (including `town`), enum values, booleans, and `last_verified` format.

## GitHub Pages view
- In GitHub: Settings -> Pages -> Build and deployment -> Source: Deploy from branch. Pick your default branch (e.g., `main`) and folder `/` so `data/` stays reachable. Save changes.
- After Pages finishes, open `https://mhlotto.github.io/413-food/docs/` to browse the data. Locally, run `python -m http.server` from repo root and open `http://localhost:8000/docs/`.
- The page fetches `docs/restaurants.yaml`, parses it client-side, and lists spots with search and filters. Click a row for a detail view (shows hours, dietary flags, notes, comments, sources).
- If you keep Pages set to `/docs`, run `python scripts/build_data.py` to copy the aggregated YAML into `docs/restaurants.yaml` before pushing changes.

## CI
- GitHub Actions workflow: `.github/workflows/validate.yml` runs `scripts/validate.py data/restaurants.yaml` on pushes and PRs.

## Future ideas
- Add a GitHub Actions workflow to run `scripts/validate.py` on PRs.
- Extend validation to flag stale `last_verified` dates and missing sources.
- Keep a `maps/` GeoJSON for quick visualization.
