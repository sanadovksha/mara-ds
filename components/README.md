# Components

Component definitions remain in Figma. This directory documents the mapping between Figma component families and production components.

## Figma component families

The current Figma file contains dedicated pages for Buttons, Form Controls, Text Fields, Navigation, Tabs, Modals, Tooltips, Sport components, Casino Cards, Banners, Bonus, Icons and other product patterns.

Use one directory per production component when code implementations are added, for example:

```text
components/
├── button/
│   └── README.md
├── text-field/
│   └── README.md
└── tabs/
    └── README.md
```

Each component document should capture:

- Figma component/page and node reference
- variants and states
- design-token dependencies
- accessibility/interaction notes
- production implementation path
- status of Figma ↔ code mapping

## Code Connect

Code Connect is not configured in this repository yet. The connected Figma account reported that Code Connect requires a Dev or Full seat on an Organization or Enterprise plan, so component-to-code mappings should be added only when that requirement is available and production component paths are known.
