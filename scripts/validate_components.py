from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "components"
REQUIRED = [
    COMPONENTS / "catalog.json",
    COMPONENTS / "button" / "contract.json",
    COMPONENTS / "text-field" / "contract.json",
    COMPONENTS / "form-controls" / "contract.json",
    COMPONENTS / "tabs" / "contract.json",
    COMPONENTS / "modal" / "contract.json",
    COMPONENTS / "dropdown" / "contract.json",
    COMPONENTS / "select" / "contract.json",
    COMPONENTS / "search-input" / "contract.json",
    COMPONENTS / "alerts" / "contract.json",
    COMPONENTS / "toasts" / "contract.json",
    COMPONENTS / "tooltips" / "contract.json",
    COMPONENTS / "sport-bar" / "contract.json",
    COMPONENTS / "sport-cards" / "contract.json",
    COMPONENTS / "sport-event-header" / "contract.json",
    COMPONENTS / "sport-event-tile" / "contract.json",
    COMPONENTS / "sport-event-tile-child" / "contract.json",
    COMPONENTS / "sport-top-card" / "contract.json",
    COMPONENTS / "sport-tournament-header" / "contract.json",
    COMPONENTS / "markets" / "contract.json",
    COMPONENTS / "casino-cards" / "contract.json",
    COMPONENTS / "bonus" / "contract.json",
    COMPONENTS / "bottomsheet-betslip" / "contract.json",
    COMPONENTS / "banners" / "contract.json",
    COMPONENTS / "navigation" / "contract.json",
    COMPONENTS / "profile" / "contract.json",
    COMPONENTS / "history-cards" / "contract.json",
    COMPONENTS / "footer" / "contract.json",
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

    expected = {
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
    }
    for folder, component_name in expected.items():
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

    print(f"Component contracts valid: {len(expected)} normalized families; catalog pages: 46")


if __name__ == "__main__":
    main()
