# Figma → GitHub sync

## Ownership

- **Figma** is the source of truth for visual component definitions, design variables, and active styles.
- **GitHub** is the reviewable/distributable snapshot used by engineering and automation.

## Current flow

```text
Figma Design System
  ├─ Core Colors
  ├─ Color System (Light/Dark × COM/RU)
  ├─ text/paint/effect/grid styles
  └─ component families
          ↓
  live export when available
          or
      exported .fig
          ↓
python scripts/export_fig_snapshot.py <file.fig> --strict-pages
          ↓
figma/offline-snapshot.json
  ├─ archive/meta hashes
  ├─ fig-kiwi version
  ├─ schema/document hashes
  └─ component-page mentions
          ↓
   normalize reviewed evidence
          ↓
GitHub pull request
  ├─ tokens/core/*.json
  ├─ tokens/semantic/*.json
  ├─ tokens/export-manifest.json
  ├─ styles/*
  ├─ components/*/contract.json
  ├─ figma/manifest.json
  ├─ figma/offline-snapshot.json
  └─ docs/*
          ↓
       CI validation
          ↓
         main
```

## Rules

1. Token and visual-component changes are made in Figma first.
2. Generated token values are not hand-edited in GitHub.
3. Figma aliases are resolved to literal values in consumer token exports.
4. Semantic token names retain the Figma `/` hierarchy.
5. Changes are reviewed through a pull request before reaching `main`.
6. Component-to-code mappings are added only when a production implementation exists.
7. `pending-verification` component contracts must not be treated as authoritative production APIs.
8. A `.fig` snapshot can establish offline observed evidence, but it cannot by itself prove current live publication status.
9. Raw string proximity is inspection evidence, not enough by itself to define a component API.

## Current source snapshot

- 47 pages
- 813 variables
- 425 `Core Colors`
- 388 `Color System` variables
- 4 semantic modes: Light/Dark × COM/RU
- 93 active text styles
- 19 active paint styles
- 14 active effect styles
- 4 active grid styles
- 46 dedicated component pages
- 39 observed component contracts
- 7 contracts still pending verification

The uploaded `.fig` archive contains additional publishable/legacy style and component records. Those are preserved as offline inventory rather than silently promoted to the active Figma API set.

## Offline `.fig` exporter

Run:

```bash
python scripts/export_fig_snapshot.py /path/to/designsystem.fig --strict-pages
```

The exporter:

- verifies the ZIP archive contains `canvas.fig` and `meta.json`;
- parses the `fig-kiwi` canvas envelope;
- decompresses the raw-deflate Kiwi schema;
- validates and decompresses the zstd document frame;
- records SHA-256 hashes and byte counts for the archive, canvas, schema, document and metadata;
- checks every component-page name listed in `figma/manifest.json`;
- writes stable two-space JSON to `figma/offline-snapshot.json`.

For evidence lookup, repeat `--query`:

```bash
python scripts/export_fig_snapshot.py designsystem.fig \
  --strict-pages \
  --query "Chips/Element" \
  --query "Slider Nav"
```

Query results contain exact byte offsets in the decompressed document payload. They are useful for repeatable inspection, but they do not automatically change component contract verification status.

The exporter intentionally shells out to the `zstd` binary rather than embedding a private parser dependency. CI contains a synthetic `.fig` regression fixture that exercises the same envelope and decompression path.

## Validation

`python scripts/validate_tokens.py` validates token coverage, partition counts, semantic modes, duplicate semantic names, supported value types, color syntax, and unresolved Figma alias objects.

`python scripts/validate_components.py` validates 46/46 component-page coverage, Schema v1 structure, source metadata, and reports how many contracts remain `pending-verification`.

`python scripts/test_export_fig_snapshot.py` validates deterministic `.fig` parsing against a generated fixture.

GitHub Actions run these checks on relevant pull requests and pushes to `main`.

## Remaining automation work

The offline `.fig` exporter is now repeatable. A **live Figma exporter** is still desirable so active variables, styles and published component metadata can be regenerated directly without relying on an exported file. Live MCP/API access is currently constrained by the available Figma plan/tool-call limit. Code Connect remains a separate follow-up once production component paths and a supported Figma seat are available.
