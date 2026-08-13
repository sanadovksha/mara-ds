from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "components"
EXPECTED = {
    "button": "Button", "text-field": "Text Field", "form-controls": "Form Controls", "tabs": "Tabs",
    "modal": "Modal", "dropdown": "DropDown", "select": "Select", "search-input": "Search Input",
    "alerts": "Alerts", "toasts": "Toasts", "tooltips": "Tooltips", "sport-bar": "Sport Bar",
    "sport-cards": "Sport Cards", "sport-event-header": "Sport Event Header", "sport-event-tile": "Sport Event Tile",
    "sport-event-tile-child": "Sport Event Tile Child", "sport-top-card": "Sport Top Card",
    "sport-tournament-header": "Sport Tournament Header", "markets": "Markets", "casino-cards": "Casino Cards",
    "bonus": "Bonus", "bottomsheet-betslip": "Bottomsheet Cards / Betslip", "banners": "Banners",
    "navigation": "Navigation", "profile": "Profile", "history-cards": "History Cards", "footer": "Footer",
    "badge": "Badge", "chips": "Chips", "labels": "Labels", "link": "Link", "date-picker": "Date Picker",
    "passcode": "Passcode", "custom-keyboard": "Custom Keyboard", "loading-spinner": "Loading, spinner",
    "timer": "Timer", "scroll": "Scroll", "slider-nav": "Slider Nav", "tile": "Tile", "support": "Support",
    "captcha": "Captcha", "3ds": "3DS", "empty-pages": "Empty Pages", "icons": "Icons",
    "password-create-block": "Password Create Block", "tooltip-new-feature": "Tooltip new feature",
}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def contains_observed(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.startswith("observed") and child not in (None, [], {}):
                return True
            if contains_observed(child):
                return True
    elif isinstance(value, list):
        return any(contains_observed(item) for item in value)
    return False


def has_recommendation_list(normalization):
    return any(
        key.startswith("recommended") and isinstance(value, list)
        for key, value in normalization.items()
    )


def main():
    catalog = load(COMPONENTS / "catalog.json")
    catalog_pages = catalog.get("componentPages")
    if not isinstance(catalog_pages, list) or len(catalog_pages) != 46:
        raise SystemExit("Catalog must contain exactly 46 component pages")
    if catalog.get("summary", {}).get("componentPages") != 46 or len(EXPECTED) != 46:
        raise SystemExit("Component coverage contract must be 46/46")

    seen_pages = set()
    pending = []
    observed = []

    for folder, component_name in EXPECTED.items():
        path = COMPONENTS / folder / "contract.json"
        if not path.exists():
            raise SystemExit(f"Missing component contract: {path.relative_to(ROOT)}")
        data = load(path)
        if data.get("component") != component_name:
            raise SystemExit(f"Unexpected component name in {path.relative_to(ROOT)}")

        source = data.get("source", {})
        page = source.get("figmaPage")
        if source.get("status") != "snapshot-derived" or not page:
            raise SystemExit(f"Invalid source metadata in {path.relative_to(ROOT)}")
        if page not in catalog_pages:
            raise SystemExit(f"Contract page is missing from catalog: {page}")
        if page in seen_pages:
            raise SystemExit(f"Duplicate contract coverage for page: {page}")
        seen_pages.add(page)

        normalization = data.get("normalization", {})
        if not isinstance(normalization, dict) or not normalization.get("notes"):
            raise SystemExit(f"Missing normalization notes in {path.relative_to(ROOT)}")
        if not has_recommendation_list(normalization):
            raise SystemExit(f"Missing normalization recommendation list in {path.relative_to(ROOT)}")

        if data.get("verification") == "pending-verification":
            pending.append(component_name)
        elif contains_observed(data):
            observed.append(component_name)
        else:
            raise SystemExit(
                f"Contract must contain observed inventory or pending-verification: {path.relative_to(ROOT)}"
            )

    if seen_pages != set(catalog_pages):
        missing = sorted(set(catalog_pages) - seen_pages)
        raise SystemExit(f"Catalog pages without contracts: {missing}")

    print("OK: 46/46 catalog pages have exactly one component contract")
    print(f"Contracts with observed snapshot inventory: {len(observed)}")
    print(f"Pending live verification: {len(pending)}")
    if pending:
        print("Pending: " + ", ".join(sorted(pending)))


if __name__ == "__main__":
    main()
