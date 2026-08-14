from __future__ import annotations

import importlib.util
import json
import shutil
import struct
import subprocess
import tempfile
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "export_fig_snapshot.py"
spec = importlib.util.spec_from_file_location("export_fig_snapshot", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def raw_deflate(data: bytes) -> bytes:
    compressor = zlib.compressobj(level=9, wbits=-15)
    return compressor.compress(data) + compressor.flush()


def zstd_compress(data: bytes) -> bytes:
    zstd = shutil.which("zstd")
    if not zstd:
        raise SystemExit("zstd is required for exporter tests")
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "payload.bin"
        target = Path(tmp) / "payload.zst"
        source.write_bytes(data)
        subprocess.run([zstd, "-q", "-f", str(source), "-o", str(target)], check=True)
        return target.read_bytes()


def make_fixture(path: Path):
    schema = b"fixture-schema-v1"
    document = "prefix ❖ Buttons middle ❖ Tabs suffix".encode("utf-8")
    schema_compressed = raw_deflate(schema)
    document_compressed = zstd_compress(document)
    canvas = (
        b"fig-kiwi"
        + struct.pack("<I", 106)
        + struct.pack("<I", len(schema_compressed))
        + schema_compressed
        + struct.pack("<I", len(document_compressed))
        + document_compressed
    )
    meta = {"file_name": "Fixture", "exported_at": "2026-01-01T00:00:00Z"}
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("canvas.fig", canvas)
        archive.writestr("meta.json", json.dumps(meta, separators=(",", ":")))
        archive.writestr("thumbnail.png", b"fixture")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fig = tmp / "fixture.fig"
        manifest = tmp / "manifest.json"
        make_fixture(fig)
        manifest.write_text(json.dumps({"componentPages": ["❖ Buttons", "❖ Tabs"]}), encoding="utf-8")

        first = module.build_report(fig, manifest, ["Buttons"])
        second = module.build_report(fig, manifest, ["Buttons"])
        assert first == second
        assert first["canvas"]["format"] == "fig-kiwi"
        assert first["canvas"]["version"] == 106
        assert first["inventory"]["componentPagesExpected"] == 2
        assert [item["count"] for item in first["inventory"]["componentPageMentions"]] == [1, 1]
        assert first["inventory"]["queries"][0]["count"] == 1
        assert module.validate_report(first, strict_pages=True) == []

    print("OK: offline .fig exporter fixture is deterministic")


if __name__ == "__main__":
    main()
