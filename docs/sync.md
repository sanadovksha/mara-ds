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
      export / normalize
          ↓
GitHub pull request
  ├─ tokens/core/*.json
  ├─ tokens/semantic/*.json
  ├─ tokens/export-manifest.json
  ├─ styles/*
  ├─ components/*/contract.json
  ├─ figma/manifest.json
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

The uploaded `.fig` archive contains additional publishable/legacy style and component records. Those are preserved as offline inventory rather than silently promoted to the active Figma API set.

## Validation

`python scripts/validate_tokens.py` validates token coverage, partition counts, semantic modes, duplicate semantic names, supported value types, color syntax, and unresolved Figma alias objects.

`python scripts/validate_components.py` validates 46/46 component-page coverage, source metadata, and reports how many contracts remain `pending-verification`.

GitHub Actions run these checks on relevant pull requests and pushes to `main`.

## Remaining automation work

A repeatable live Figma exporter is still desirable so future updates can regenerate the repository deterministically without relying on a manually uploaded `.fig` snapshot. Code Connect remains a separate follow-up once production component paths and a supported Figma seat are available.
