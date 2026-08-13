# Components

Component definitions remain in Figma. This directory documents the mapping between Figma component families and production components.

## Inventory

- `catalog.json` — component-page catalog and snapshot counters
- `variant-property-index.md` — compact index of variant/property patterns extracted from the uploaded `.fig` snapshot

The live Figma manifest contains 46 dedicated component pages. The uploaded `.fig` snapshot contains 5,897 indexed variant nodes across 168 distinct property signatures. Snapshot counts may include legacy or unpublished variants, so Figma remains the source of truth for what is currently published.

## Normalized contracts

The first component-family contracts are now documented separately:

- `button/contract.json`
- `text-field/contract.json`
- `form-controls/contract.json`
- `tabs/contract.json`

Each contract keeps **observed Figma values** separate from **normalization recommendations**. Recommended names are not treated as changes to the Figma source until they are explicitly applied there.

These contracts are intended to become the stable translation layer between Figma and production code. Future component contracts should use the same structure: source, observed variants/properties, normalization notes, and eventually production implementation / Code Connect metadata.

## Figma component families

The current Figma file contains dedicated pages for Buttons, Form Controls, Text Fields, Navigation, Tabs, Modals, Tooltips, Sport components, Casino Cards, Banners, Bonus, Icons and other product patterns.

Each component document should capture:

- Figma component/page and node reference
- variants and states
- design-token dependencies
- accessibility/interaction notes
- production implementation path
- status of Figma ↔ code mapping

## Naming cleanup

The snapshot shows consistent properties such as `State`, `Size` and `Type`, but also legacy generic properties such as `Property 1`. Generic properties should be treated as cleanup candidates and should not be copied directly into production component APIs.

Examples already found during normalization:

- Button has a mature `Size / State / Style / Theme / Type` signature.
- Text Field contains the lowercase property `outlined`; `Outlined` is suggested only as a future normalization.
- Checkbox uses a property named `Checkbox` with `Off / On`; `Checked` is a possible production-friendly mapping, not a Figma rename.
- Tabs contains a `Dark Mode` property at container level; production theming should normally come from the DS theme context rather than a public Tabs prop.
- Radio patterns need a separate cleanup pass because multiple property signatures coexist in the snapshot.

## Code Connect

Code Connect is not configured in this repository yet. The connected Figma account reported that Code Connect requires a Dev or Full seat on an Organization or Enterprise plan, so component-to-code mappings should be added only when that requirement is available and production component paths are known.
