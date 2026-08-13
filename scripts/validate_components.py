from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "components"

EXPECTED = {
    "button": "Button",
    "text-field": "Text Field",
    "form-controls": "Form Controls",
    "tabs": "Tabs",
    "modal": "Modal",
    "dropdown": "DropDown",
    "select": "Select",
    "search-input": "Search Input",
    "alerts": "Alerts",
    "toasts": "Toasts",
    "tooltips": "Tooltips",
    "sport-bar": "Sport Bar",
    "sport-cards": "Sport Cards",
    "sport-event-header": "Sport Event Header",
    "sport-event-tile": "Sport Event Tile",
    "sport-event-tile-child": "Sport Event Tile Child",
    "sport-top-card": "Sport Top Card",
    "sport-tournament-header": "Sport Tournament Header",
    "markets": "Markets",
    "casino-cards": "Casino Cards",
    "bonus": "Bonus",
    "bottomsheet-betslip": "Bottomsheet Cards / Betslip",
    "banners": "Banners",
    "navigation": "Navigation",
    "profile": "Profile",
    "history-cards": "History Cards",
    "footer": "Footer",
    "badge": "Badge",
    "chips": "Chips",
    "labels": "Labels",
    "link": "Link",
    "date-picker": "Date Picker",
    "passcode": "Passcode",
    "custom-keyboard": "Custom Keyboard",
    "loading-spinner": "Loading, spinner",
    "timer": "Timer",
    "scroll": "Scroll",
    "slider-nav": "Slider Nav",
    "tile": "Tile",
    "support": "Support",
    "captcha": "Captcha",
    "3ds": "3DS",
    "empty-pages": "Empty Pages",
}

REQUIRED = [COMPONENTS / "catalog.json"] + [
    COMPONENTS / folder / "contract.json" for folder in EXPECTED
]


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def main() -> None:
    missing = [p.relative_to(ROOT) for p in REQUIRED if not p.exists()]
    if missing:
        raise SystemExit("Missing component files: " + ", ".join(map(str, missing)))

    catalog = load_json(REQUIRED[0])
    if catalog.get("summary", {}).get("componentPages") != 46:
        raise SystemExit("Component page count mismatch: expected 46")

    for folder, component_name in EXPECTED.items():
        path = COMPONENTS / folder / "contract.json"
        data = load_json(path)
        if data.get("component") != component_name:
            raise SystemExit(f"Unexpected component name in {path.relative_to(ROOT)}")
        source = data.get("source", {})
        if source.get("status") != "snapshot-derived":
            raise SystemExit(f"Missing snapshot-derived status in {path.relative_to(ROOT)}")
        if not source.get("figmaPage"):
            raise SystemExit(f"Missing Figma page in {path.relative_to(ROOT)}")
        if not data.get("normalization", {}).get("notes"):
            raise SystemExit(f"Missing normalization notes in {path.relative_to(ROOT)}")

    print(f"Component contracts valid: {len(EXPECTED)} normalized families; catalog pages: 46")


if __name__ == "__main__":
    main()
