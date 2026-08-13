from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "tokens", ROOT / "styles", ROOT / "components", ROOT / "figma"]


def main():
    changed = 0
    for folder in TARGETS:
        for path in sorted(folder.rglob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            formatted = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
            if path.read_text(encoding="utf-8") != formatted:
                path.write_text(formatted, encoding="utf-8")
                changed += 1
                print(f"formatted {path.relative_to(ROOT)}")
    print(f"JSON files reformatted: {changed}")


if __name__ == "__main__":
    main()
