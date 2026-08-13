# Figma → GitHub sync

## Ownership

- **Figma** is the source of truth for visual component definitions and design variables.
- **GitHub** is the reviewable/distributable representation used by engineering and automation.

## Flow

```text
Figma Design System
  ├─ Core Colors
  ├─ Color System (Light/Dark × COM/RU)
  ├─ text/paint/effect/grid styles
  └─ component families
          ↓
      export/normalize
          ↓
GitHub pull request
  ├─ tokens/*.json
  ├─ figma/manifest.json
  ├─ components/*
  └─ docs/*
```

## Rules

1. Token values are changed in Figma first.
2. GitHub token exports are generated artifacts; do not edit them manually.
3. Figma aliases should be resolved to literal values in exported consumer files.
4. Semantic token names retain their Figma hierarchy.
5. Changes are reviewed through a pull request before reaching `main`.
6. Component-to-code mappings are added only when a production implementation exists.

## Current source snapshot

At initial import the Figma file contains:

- 47 pages
- 813 variables
- 425 `Core Colors`
- 388 `Color System` variables
- 4 semantic modes: Light/Dark × COM/RU
- 93 text styles
- 19 paint styles
- 14 effect styles
- 4 grid styles

## Next automation step

Add a repeatable exporter that writes `tokens/core-colors.json` and `tokens/color-system.json` from Figma, then validates generated output in CI. The exporter should fail on duplicate normalized token names, unresolved aliases, or unsupported value types.
