import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tokens" / "export-manifest.json"


def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def token_count(obj):
    if isinstance(obj, dict):
        if "tokens" in obj and isinstance(obj["tokens"], dict):
            return len(obj["tokens"])
        return len(obj)
    raise ValueError("Token file root must be an object")


def main():
    manifest = load(MANIFEST)
    expected_total = manifest["totalVariables"]
    core_expected = manifest["coreColors"]["total"]
    semantic_expected = manifest["semantic"]["total"]

    core_count = 0
    for rel in manifest["coreColors"]["files"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing core token file: {rel}")
        core_count += token_count(load(path))

    semantic_count = 0
    semantic_modes = manifest["modes"]
    for rel in manifest["semantic"]["files"]:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"Missing semantic token file: {rel}")
        data = load(path)
        tokens = data.get("tokens", data)
        semantic_count += len(tokens)
        for name, value in tokens.items():
            if not isinstance(value, dict):
                raise SystemExit(f"Semantic token is not an object: {name}")
            missing = [mode for mode in semantic_modes if mode not in value]
            if missing:
                raise SystemExit(f"Semantic token {name} misses modes: {missing}")

    if core_count != core_expected:
        raise SystemExit(f"Core token count mismatch: {core_count} != {core_expected}")
    if semantic_count != semantic_expected:
        raise SystemExit(f"Semantic token count mismatch: {semantic_count} != {semantic_expected}")
    if core_count + semantic_count != expected_total:
        raise SystemExit(
            f"Total token count mismatch: {core_count + semantic_count} != {expected_total}"
        )

    print(f"OK: {core_count} core + {semantic_count} semantic = {expected_total} variables")
    print(f"OK: semantic tokens include all {len(semantic_modes)} modes")


if __name__ == "__main__":
    main()
