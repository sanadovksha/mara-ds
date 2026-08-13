# Design tokens

Figma is the source of truth for design tokens. GitHub contains generated consumer snapshots that are reviewed through pull requests.

## Collections

### Core Colors

425 primitive variables. Product UI should normally consume semantic tokens rather than reference these primitives directly.

### Color System

388 semantic variables with four modes:

- `Light • COM`
- `Dark • COM`
- `Light • RU`
- `Dark • RU`

Figma aliases are resolved to literal values in the exported consumer snapshot while token names preserve the Figma `/` hierarchy.

## Export structure

```text
tokens/
├── export-manifest.json
├── core/
│   ├── common-a.json
│   ├── common-b.json
│   ├── light.json
│   └── dark.json
└── semantic/
    ├── foundation.json
    ├── accents.json
    ├── ui-controls.json
    └── components.json
```

`export-manifest.json` is the coverage contract for the export. It records the expected Core, semantic, partition, mode, and total counts.

Current coverage:

- Core Colors: 425
- Color System: 388
- Total variables: 813
- Semantic partitions: 101 foundation + 44 accents + 113 UI controls + 130 components

## Editing rule

Do not hand-edit generated token values in GitHub. Change the source variable in Figma, regenerate the export, and review the resulting diff in a pull request.

Run `python scripts/validate_tokens.py` to validate coverage, semantic modes, duplicate names, supported value types, color formatting, and unresolved alias objects.
