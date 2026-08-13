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
    return json.loads(path.read_text(encoding="utf-8"))


def contains_observed(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.startswith("observed") and child not in (None, [], {}):
                return True
            if contains_observed(child):
                return True
    if isinstance(value, list):
        return any(contains_observed(item) for item in value)
    return False


def is_pending(data):
    value = data.get("verification")
    return value == "pending-verification" or (
        isinstance(value, dict) and value.get("status") == "pending-verification"
    )


def main():
    catalog = load(COMPONENTS / "catalog.json")
    pages = catalog.get("componentPages")
    if not isinstance(pages, list) or len(pages) != 46 or len(EXPECTED) != 46:
        raise SystemExit("Component coverage must be 46/46")

    seen = set()
    pending = []
    observed = []
    for folder, name in EXPECTED.items():
        path = COMPONENTS / folder / "contract.json"
        if not path.exists():
            raise SystemExit(f"Missing contract: {path.relative_to(ROOT)}")
        data = load(path)
        if data.get("component") != name:
            raise SystemExit(f"Unexpected component name: {path.relative_to(ROOT)}")
        source = data.get("source", {})
        page = source.get("figmaPage")
        if source.get("status") != "snapshot-derived" or page not in pages or page in seen:
            raise SystemExit(f"Invalid or duplicate source page: {path.relative_to(ROOT)}")
        seen.add(page)

        normalization = data.get("normalization", {})
        if not normalization.get("notes"):
            raise SystemExit(f"Missing normalization notes: {path.relative_to(ROOT)}")
        if not any(k.startswith("recommended") and isinstance(v, list) for k, v in normalization.items()):
            raise SystemExit(f"Missing normalization recommendation list: {path.relative_to(ROOT)}")

        if is_pending(data):
            pending.append(name)
        elif contains_observed(data):
            observed.append(name)
        else:
            raise SystemExit(f"No observed inventory or pending status: {path.relative_to(ROOT)}")

    if seen != set(pages):
        raise SystemExit(f"Catalog pages without contracts: {sorted(set(pages) - seen)}")

    print("OK: 46/46 catalog pages have exactly one contract")
    print(f"Observed snapshot contracts: {len(observed)}")
    print(f"Pending live verification: {len(pending)}")
    if pending:
        print("Pending: " + ", ".join(sorted(pending)))


if __name__ == "__main__":
    main()
