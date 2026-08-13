from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tokens" / "export-manifest.json"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")
MODES = ["Light • COM", "Dark • COM", "Light • RU", "Dark • RU"]
PARTITION_KEYS = {"ui-controls": "uiControls"}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def tokens(path: Path):
    data = load(path)
    if not isinstance(data, dict):
        raise SystemExit(f"Root must be an object: {path.relative_to(ROOT)}")
    value = data.get("tokens", data)
    if not isinstance(value, dict):
        raise SystemExit(f"Token map must be an object: {path.relative_to(ROOT)}")
    return value


def literal(value, where):
    if isinstance(value, (dict, list)) or value is None:
        raise SystemExit(f"Non-literal token value in {where}: {value!r}")
    if not isinstance(value, (str, bool, int, float)):
        raise SystemExit(f"Unsupported token type in {where}: {type(value).__name__}")
    if isinstance(value, str) and value.startswith("#") and not HEX.fullmatch(value):
        raise SystemExit(f"Invalid hex color in {where}: {value}")


def main():
    manifest = load(MANIFEST)
    if manifest.get("modes") != MODES:
        raise SystemExit(f"Unexpected modes: {manifest.get('modes')!r}")

    core_cfg = manifest["coreColors"]
    sem_cfg = manifest["semantic"]

    core_seen = set()
    core_count = 0
    for rel in core_cfg["files"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing core file: {rel}")
        current = tokens(path)
        for name, value in current.items():
            if name in core_seen:
                raise SystemExit(f"Duplicate core token: {name}")
            core_seen.add(name)
            literal(value, f"{rel}:{name}")
        core_count += len(current)

    sem_seen = set()
    sem_count = 0
    partitions = sem_cfg["partitions"]
    for rel in sem_cfg["files"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing semantic file: {rel}")
        current = tokens(path)
        part = PARTITION_KEYS.get(path.stem, path.stem)
        if len(current) != partitions.get(part):
            raise SystemExit(f"Partition count mismatch for {part}: {len(current)} != {partitions.get(part)}")
        for name, values in current.items():
            if name in sem_seen:
                raise SystemExit(f"Duplicate semantic token: {name}")
            sem_seen.add(name)
            if not isinstance(values, dict) or list(values) != MODES:
                raise SystemExit(f"Unexpected semantic modes for {name}: {list(values) if isinstance(values, dict) else values!r}")
            for mode, value in values.items():
                literal(value, f"{rel}:{name}:{mode}")
        sem_count += len(current)

    if core_count != core_cfg["total"]:
        raise SystemExit(f"Core count mismatch: {core_count} != {core_cfg['total']}")
    if sem_count != sem_cfg["total"] or sem_cfg.get("exported") != sem_count:
        raise SystemExit(f"Semantic count mismatch: {sem_count} != {sem_cfg['total']}")
    if core_count + sem_count != manifest["totalVariables"]:
        raise SystemExit("Combined token count does not match manifest")

    print(f"OK: {core_count} core + {sem_count} semantic = {manifest['totalVariables']}")
    print("OK: names are unique, partitions and modes match, values are literals")


if __name__ == "__main__":
    main()
