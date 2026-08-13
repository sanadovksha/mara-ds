from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "components"
SCHEMA_VERSION = 1
REQUIRED_KEYS = {
    "schemaVersion", "component", "source", "verification", "variants",
    "subcomponents", "evidence", "normalization",
}
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


def main():
    catalog = load(COMPONENTS / "catalog.json")
    pages = catalog.get("componentPages")
    if not isinstance(pages, list) or len(pages) != 46 or len(EXPECTED) != 46:
        raise SystemExit("Component coverage must be 46/46")

    seen = set()
    observed = []
    pending = []

    for folder, expected_name in EXPECTED.items():
        path = COMPONENTS / folder / "contract.json"
        if not path.exists():
            raise SystemExit(f"Missing contract: {path.relative_to(ROOT)}")
        data = load(path)

        if set(data) != REQUIRED_KEYS:
            missing = sorted(REQUIRED_KEYS - set(data))
            extra = sorted(set(data) - REQUIRED_KEYS)
            raise SystemExit(f"Schema v1 key mismatch in {path.relative_to(ROOT)}; missing={missing}, extra={extra}")
        if data["schemaVersion"] != SCHEMA_VERSION:
            raise SystemExit(f"Unexpected schemaVersion in {path.relative_to(ROOT)}")
        if data["component"] != expected_name:
            raise SystemExit(f"Unexpected component name in {path.relative_to(ROOT)}")

        source = data["source"]
        if not isinstance(source, dict):
            raise SystemExit(f"Invalid source in {path.relative_to(ROOT)}")
        page = source.get("figmaPage")
        if source.get("snapshot") != "designsystem-opt.fig" or source.get("status") != "snapshot-derived":
            raise SystemExit(f"Invalid source metadata in {path.relative_to(ROOT)}")
        if page not in pages or page in seen:
            raise SystemExit(f"Invalid or duplicate source page in {path.relative_to(ROOT)}")
        seen.add(page)

        verification = data["verification"]
        if not isinstance(verification, dict):
            raise SystemExit(f"verification must be an object in {path.relative_to(ROOT)}")
        status = verification.get("status")
        if status not in {"observed", "pending-verification"} or not verification.get("reason"):
            raise SystemExit(f"Invalid verification in {path.relative_to(ROOT)}")

        for key in ("variants", "subcomponents", "evidence"):
            if not isinstance(data[key], dict):
                raise SystemExit(f"{key} must be an object in {path.relative_to(ROOT)}")

        normalization = data["normalization"]
        if not isinstance(normalization, dict):
            raise SystemExit(f"Invalid normalization in {path.relative_to(ROOT)}")
        if set(normalization) != {"recommendedPropertyNames", "notes", "details"}:
            raise SystemExit(f"Normalization schema mismatch in {path.relative_to(ROOT)}")
        if not isinstance(normalization["recommendedPropertyNames"], list):
            raise SystemExit(f"recommendedPropertyNames must be a list in {path.relative_to(ROOT)}")
        if not isinstance(normalization["notes"], list) or not normalization["notes"]:
            raise SystemExit(f"notes must be a non-empty list in {path.relative_to(ROOT)}")
        if not isinstance(normalization["details"], dict):
            raise SystemExit(f"details must be an object in {path.relative_to(ROOT)}")

        if status == "observed":
            if not any(data[key] for key in ("variants", "subcomponents", "evidence")):
                raise SystemExit(f"Observed contract has no evidence in {path.relative_to(ROOT)}")
            observed.append(expected_name)
        else:
            pending.append(expected_name)

    if seen != set(pages):
        raise SystemExit(f"Catalog pages without contracts: {sorted(set(pages) - seen)}")

    print("OK: 46/46 contracts conform to Component Contract Schema v1")
    print(f"Observed snapshot contracts: {len(observed)}")
    print(f"Pending live verification: {len(pending)}")
    if pending:
        print("Pending: " + ", ".join(sorted(pending)))


if __name__ == "__main__":
    main()
