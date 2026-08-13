# Components

Component definitions remain in Figma. This directory documents the mapping between Figma component families and production components.

## Inventory

- `catalog.json` — component-page catalog and snapshot counters
- `variant-property-index.md` — compact index of variant/property patterns extracted from the uploaded `.fig` snapshot

The live Figma manifest contains 46 dedicated component pages. The uploaded `.fig` snapshot contains 5,897 indexed variant nodes across 168 distinct property signatures. Snapshot counts may include legacy or unpublished variants, so Figma remains the source of truth for what is currently published.

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

## Naming cleanup

The snapshot shows consistent properties such as `State`, `Size` and `Type`, but also legacy generic properties such as `Property 1`. Generic properties should be treated as cleanup candidates and should not be copied directly into production component APIs.

## Code Connect

Code Connect is not configured in this repository yet. The connected Figma account reported that Code Connect requires a Dev or Full seat on an Organization or Enterprise plan, so component-to-code mappings should be added only when that requirement is available and production component paths are known.
