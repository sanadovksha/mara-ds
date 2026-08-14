# Mara Design System

Reviewable design-system snapshot for Marathonbet.

## Source of truth

- **Figma** is the source of truth for visual component definitions, variables, and styles.
- **GitHub** stores exported snapshots, normalized component contracts, validation scripts, and synchronization documentation.

Figma file: `Design System` (`cUFnNueMAuBe5RKObSu6c7`).

## Current snapshot

- 47 Figma pages
- 813 variables
  - 425 Core Colors
  - 388 semantic Color System variables
- 4 semantic modes: Light/Dark × COM/RU
- 93 active text styles
- 19 active paint styles
- 14 active effect styles
- 4 active grid styles
- 46 dedicated component pages covered by component contracts
- 39 component contracts with observed snapshot evidence
- 7 component contracts still pending verification

The uploaded `.fig` snapshot also contains publishable/legacy records that are kept separately from the active Figma API inventory.

## Repository structure

```text
figma/
  manifest.json
  offline-snapshot.json

tokens/
  export-manifest.json
  core/
  semantic/

styles/
  inventory.json
  file-snapshot/

components/
  catalog.json
  variant-property-index.md
  <family>/contract.json

docs/
  sync.md

scripts/
  export_fig_snapshot.py
  test_export_fig_snapshot.py
  format_json.py
  validate_tokens.py
  validate_components.py
```

## Component contract status

A Schema v1 component contract is either `observed` or `pending-verification`. `pending-verification` means the component family is confirmed, but the available evidence cannot reliably distinguish the top-level public API from nested or legacy variants.

Offline `.fig` evidence can promote a contract to `observed` only when the component-set relationship is unambiguous. Offline evidence does not prove that the same component is currently published in the live Figma library.

## Local commands

```bash
python scripts/export_fig_snapshot.py /path/to/designsystem.fig --strict-pages
python scripts/format_json.py
python scripts/validate_tokens.py
python scripts/validate_components.py
python scripts/test_export_fig_snapshot.py
```

`export_fig_snapshot.py` parses the `.fig` archive envelope, validates the `fig-kiwi` canvas structure, decompresses the raw-deflate schema and zstd document payload, records deterministic hashes, and checks component-page mentions from `figma/manifest.json`. Use `--query "Exact component/set name"` for repeatable binary evidence lookup.

`format_json.py` gives generated JSON stable two-space formatting so future pull-request diffs are readable. Run it after regenerating snapshot files.

Validation and exporter regression tests run in GitHub Actions on relevant pull requests and pushes to `main`.

## Change workflow

1. Make design-token and visual-component changes in Figma first.
2. Export a fresh `.fig` when live API access is unavailable.
3. Run `export_fig_snapshot.py` to regenerate `figma/offline-snapshot.json`.
4. Review changed hashes, page coverage, queries, tokens, styles, and component evidence.
5. Run the formatter and validation scripts.
6. Review changes through a pull request.
7. Keep generated token values out of manual GitHub edits.

See [`docs/sync.md`](docs/sync.md) for the synchronization contract and known limitations.
