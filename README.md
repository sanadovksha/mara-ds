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

The uploaded `.fig` snapshot also contains publishable/legacy records that are kept separately from the active Figma API inventory.

## Repository structure

```text
figma/
  manifest.json

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
  validate_tokens.py
  validate_components.py
```

## Component contract status

A component contract can contain a verified observed variant signature or be marked `pending-verification`. `pending-verification` means the component family is confirmed, but the offline `.fig` snapshot cannot reliably distinguish the current top-level public API from nested or legacy variants.

Do not treat `pending-verification` contracts as production component APIs until they are checked against live published Figma metadata.

## Validation

Run locally:

```bash
python scripts/validate_tokens.py
python scripts/validate_components.py
```

The same checks run in GitHub Actions on relevant pull requests and on pushes to `main`.

## Change workflow

1. Make design-token and visual-component changes in Figma first.
2. Regenerate/export the GitHub snapshot.
3. Review changes through a pull request.
4. Keep generated token values out of manual GitHub edits.

See [`docs/sync.md`](docs/sync.md) for the synchronization contract and known limitations.
