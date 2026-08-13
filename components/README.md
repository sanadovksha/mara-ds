# Components

Component definitions remain in Figma. This directory is the reviewable translation layer between Figma component families and future production implementations.

## Inventory

- `catalog.json` — 46 component pages and snapshot counters
- `variant-property-index.md` — compact index of variant/property patterns extracted from the uploaded `.fig` snapshot
- `<family>/contract.json` — one normalized contract for each component page

The uploaded `.fig` snapshot contains 5,897 indexed variant nodes across 168 distinct property signatures. Snapshot counts may include legacy or unpublished variants, so Figma remains the source of truth for what is currently published.

## Component Contract Schema v1

All 46 component contracts use one top-level shape:

```json
{
  "schemaVersion": 1,
  "component": "Button",
  "source": {
    "figmaPage": "❖ Buttons",
    "snapshot": "designsystem-opt.fig",
    "status": "snapshot-derived"
  },
  "verification": {
    "status": "observed",
    "reason": "..."
  },
  "variants": {},
  "subcomponents": {},
  "evidence": {},
  "normalization": {
    "recommendedPropertyNames": [],
    "notes": [],
    "details": {}
  }
}
```

### Verification status

`verification.status` has two allowed values:

- `observed` — usable variant/property evidence was isolated from the uploaded snapshot.
- `pending-verification` — the family/page is confirmed, but the public component API still requires live published Figma metadata.

A pending contract must not be treated as a production component API.

### Data placement

- `variants` contains directly observed top-level variant/property data.
- `subcomponents` keeps nested component sets separate instead of flattening them into one oversized API.
- `evidence` stores partial, related or supporting snapshot observations that should not be promoted to top-level props.
- `normalization.recommendedPropertyNames` contains proposed code/design-system naming, not silent source renames.
- `normalization.notes` explains limitations and cleanup decisions.
- `normalization.details` stores structured normalization metadata when needed.

Legacy top-level fields such as `observedVariantSignature`, `observedVariants`, `observedPatterns` and string-form `verification` are no longer valid in Schema v1.

`python scripts/validate_components.py` enforces this structure for all 46 contracts.

## Naming cleanup

The snapshot shows consistent properties such as `State`, `Size` and `Type`, but also legacy generic properties such as `Property 1`. Generic properties remain cleanup candidates and are not automatically copied into production component APIs.

Examples:

- Button has a mature `Size / State / Style / Theme / Type` signature.
- Text Field contains the lowercase source property `outlined`; `Outlined` is only the recommended normalized name.
- Checkbox uses the source property `Checkbox` with `Off / On`; `Checked` is a production-friendly recommendation.
- Tabs contains a container-level `Dark Mode`; production theming should normally come from theme context.
- Radio patterns remain separate evidence because multiple legacy signatures coexist.

## Code Connect

Code Connect is not configured yet. Add component-to-code mappings only when production implementation paths are known and the connected Figma account supports the required Code Connect capability.
