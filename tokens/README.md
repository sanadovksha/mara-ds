# Design tokens

Figma is the current source of truth for design tokens.

## Collections

### Core Colors

Primitive color palette. 425 variables in Figma, one mode.

These values should not normally be referenced directly by product UI. Semantic tokens in `Color System` should reference the primitives.

### Color System

388 semantic variables with four modes:

- `Light • COM`
- `Dark • COM`
- `Light • RU`
- `Dark • RU`

Examples include `Base/Surface`, `Text or Icons/Primary`, `Button/Solid/Primary`, and accent/status colors.

## Export format

Generated token exports should preserve the Figma hierarchy using `/` as the semantic path separator and resolve Figma aliases to literal primitive values for consumption outside Figma.

Planned generated files:

```text
tokens/
├── core-colors.json
└── color-system.json
```

Do not hand-edit generated token values in GitHub. Change the source variable in Figma and regenerate the export.
