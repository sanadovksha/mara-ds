from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import tempfile
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "figma" / "manifest.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decompress_zstd(data: bytes) -> bytes:
    zstd = shutil.which("zstd")
    if not zstd:
        raise SystemExit("zstd is required to inspect the .fig canvas payload")
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "payload.zst"
        target = Path(tmp) / "payload.bin"
        source.write_bytes(data)
        subprocess.run([zstd, "-d", "-q", "-f", str(source), "-o", str(target)], check=True)
        return target.read_bytes()


def parse_canvas(canvas: bytes):
    if not canvas.startswith(b"fig-kiwi"):
        raise SystemExit("Unsupported canvas: expected fig-kiwi header")
    if len(canvas) < 20:
        raise SystemExit("Invalid canvas.fig: file is too short")

    version = struct.unpack_from("<I", canvas, 8)[0]
    schema_compressed_length = struct.unpack_from("<I", canvas, 12)[0]

    inflater = zlib.decompressobj(-15)
    schema_input = canvas[16:]
    schema = inflater.decompress(schema_input) + inflater.flush()
    schema_consumed = len(schema_input) - len(inflater.unused_data)
    if schema_consumed != schema_compressed_length:
        raise SystemExit(
            f"Schema length mismatch: header={schema_compressed_length}, consumed={schema_consumed}"
        )

    rest = inflater.unused_data
    if len(rest) < 8:
        raise SystemExit("Invalid canvas.fig: missing document payload")

    document_compressed_length = struct.unpack_from("<I", rest, 0)[0]
    document_compressed = rest[4:4 + document_compressed_length]
    if len(document_compressed) != document_compressed_length:
        raise SystemExit("Invalid canvas.fig: truncated document payload")
    if document_compressed[:4] != b"\x28\xb5\x2f\xfd":
        raise SystemExit("Unsupported document payload: expected zstd frame")

    trailing = rest[4 + document_compressed_length:]
    if trailing:
        raise SystemExit(f"Invalid canvas.fig: unexpected trailing bytes ({len(trailing)})")

    return {
        "format": "fig-kiwi",
        "version": version,
        "schema": schema,
        "schemaCompressedLength": schema_compressed_length,
        "document": decompress_zstd(document_compressed),
        "documentCompressedLength": document_compressed_length,
    }


def occurrences(data: bytes, text: str):
    needle = text.encode("utf-8")
    offsets = []
    start = 0
    while True:
        index = data.find(needle, start)
        if index < 0:
            return offsets
        offsets.append(index)
        start = index + len(needle)


def build_report(fig_path: Path, manifest_path: Path, queries: list[str] | None = None):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive_bytes = fig_path.read_bytes()

    with zipfile.ZipFile(fig_path) as archive:
        names = sorted(archive.namelist())
        if "canvas.fig" not in names or "meta.json" not in names:
            raise SystemExit("Unsupported .fig archive: canvas.fig and meta.json are required")
        canvas = archive.read("canvas.fig")
        meta_raw = archive.read("meta.json")
        meta = json.loads(meta_raw.decode("utf-8"))
        image_entries = [name for name in names if name.startswith("images/") and name != "images/"]

    parsed = parse_canvas(canvas)
    document = parsed.pop("document")
    schema = parsed.pop("schema")

    page_mentions = []
    for page in manifest.get("componentPages", []):
        matches = occurrences(document, page)
        page_mentions.append({"name": page, "count": len(matches), "offsets": matches[:20]})

    query_results = []
    for query in queries or []:
        matches = occurrences(document, query)
        query_results.append({"query": query, "count": len(matches), "offsets": matches[:100]})

    return {
        "exportVersion": 1,
        "source": {
            "file": fig_path.name,
            "archiveSha256": sha256(archive_bytes),
            "archiveBytes": len(archive_bytes),
            "meta": meta,
        },
        "archive": {
            "entries": len(names),
            "imageEntries": len(image_entries),
            "canvasBytes": len(canvas),
            "canvasSha256": sha256(canvas),
            "metaSha256": sha256(meta_raw),
        },
        "canvas": {
            **parsed,
            "schemaBytes": len(schema),
            "schemaSha256": sha256(schema),
            "documentBytes": len(document),
            "documentSha256": sha256(document),
        },
        "inventory": {
            "componentPagesExpected": len(manifest.get("componentPages", [])),
            "componentPageMentions": page_mentions,
            "queries": query_results,
        },
        "notes": [
            "This is an offline binary snapshot, not a statement about current Figma publication status.",
            "String mentions are inspection evidence only and do not prove top-level component ownership.",
            "Promote a contract to observed only when component-set evidence is unambiguous.",
        ],
    }


def validate_report(report, strict_pages: bool):
    pages = report["inventory"]["componentPageMentions"]
    missing = [item["name"] for item in pages if item["count"] == 0]
    if strict_pages and missing:
        raise SystemExit("Expected component pages not found in payload: " + ", ".join(missing))
    return missing


def main():
    parser = argparse.ArgumentParser(description="Export deterministic metadata from a Figma .fig archive")
    parser.add_argument("fig", type=Path, help="Path to a .fig archive")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=ROOT / "figma" / "offline-snapshot.json")
    parser.add_argument("--query", action="append", default=[], help="Exact UTF-8 string to locate in the document payload")
    parser.add_argument("--strict-pages", action="store_true", help="Fail when a manifest component page is not found in the payload")
    args = parser.parse_args()

    report = build_report(args.fig, args.manifest, args.query)
    missing = validate_report(report, args.strict_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {args.output}")
    print(f"Archive SHA-256: {report['source']['archiveSha256']}")
    print(f"Canvas format: {report['canvas']['format']} v{report['canvas']['version']}")
    print(f"Document bytes: {report['canvas']['documentBytes']}")
    print(f"Component pages found: {len(report['inventory']['componentPageMentions']) - len(missing)}/{len(report['inventory']['componentPageMentions'])}")


if __name__ == "__main__":
    main()
