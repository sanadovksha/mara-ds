# Variant property index

Source: `designsystem-opt.fig` (offline snapshot).

This index is derived from variant signatures embedded in the uploaded `.fig` canvas. It is a snapshot inventory, not an assertion that every legacy variant is currently published in Figma.

- Indexed variant nodes: **5,897**
- Distinct property signatures: **168**

## Most common property signatures

### `Size` + `Type` — 1,405 variants
- Size: 21 values, including `40px`, `44 / M`, `44px`, `48px`, `L`, `M`, `S`, `XL`, `XS`
- Type: 46 values, including `Active`, `Additional`, `App-COM`, `App-RU`, `Bonus`, `Default`, `Disable`, `Error`

### `Type` — 383 variants
244 distinct values. This group spans many unrelated component families, so it should not be normalized globally.

### `State` — 292 variants
124 distinct state values, including `Active`, `Default`, `Disabled`, `Error`, `Focused`, `Hover`, `Loading`, `Regular`, `Selected`, `Success`, `Warning`.

### `Size` + `State` + `Style` + `Theme` + `Type` — 288 variants
- Size: `32 / S`, `44 / M`
- State: `Disabled`, `Loading`, `Normal`
- Style: `Color`, `Commerce`, `Outline`, `Primary`, `Secondary`, `Tertiary`
- Theme: `Day`, `Night`
- Type: `Icon only`, `Left icon`, `Right icon`, `Text`

### `Size` + `State` — 278 variants
18 size values and 30 state values. Common states include `Active`, `Default`, `Disable`, `Error`, `Filled`, `Focused`, `Hover`, `Opened`, `Pressed`.

### `State` + `Type` — 206 variants
- State: 33 values
- Type: 35 values
- Examples include card, checkbox, tabs and sport-specific variants.

### `Sport` — 110 variants
105 sport values were found, including `Football`, `Basketball`, `Tennis`, `Hockey`, `Volleyball`, `e-Sports` and others.

### `Active` + `Size` + `State` — 106 variants
- Active: `Off`, `On`
- Size: `L`, `M`, `Medium`, `S`, `Small`
- State: `Default`, `Disable`, `Error`, `Hover`, `Regular`

### `Checkbox` + `State` + `Type` — 96 variants
- Checkbox: `Off`, `On`
- State: `Disabled`, `Focused`, `Hover`, `Overflow`, `Pressed`, `Regular`
- Type: `Default`, `Selected`

### `Fill` + `Size` + `Type` — 96 variants
- Fill: `Mono`, `Theme`
- Size: 8 values from `xxxsmall` to `xlarge`
- Type: `Active`, `Default`, `Disable`, `Focused`, `Hover`, `Loader`

### `Name` + `State` — 96 variants
This group contains social-network icons: Facebook, Instagram, LinkedIn, MAX, Telegram, Viber, Vk, WeChat, Weibo, Whatsapp, X social and Youtube, with `Regular`, `Hover`, `Active` states.

### `Arrow` + `Color` + `Scheme` + `State` + `Text` + `Type` — 92 variants
Contains navigation/service-menu style combinations with Light/Dark/Mono schemes and Default/Hover/Focused/Active states.

### `Size` + `State` + `Type` — 86 variants
Includes Desktop/Mobile sizing and `Favs`, `Live`, `Mono`, `Prematch`, `Theme` types.

### `Indication` + `Type` — 75 variants
- Indication: `Green`, `No`, `Red`
- Type: `Active`, `Active-Hover`, `Default`, `Default-Hover`, `Disable`, `Nothing`, `Nothing Desktop`, `Nothing Mobile`

## Interpretation

The snapshot shows that the design system contains both mature property naming (`State`, `Size`, `Type`) and generic/legacy naming such as `Property 1`. The latter should be treated as cleanup candidates rather than copied into production APIs.

For production component documentation, each family should get its own normalized contract (for example Button, Text Field, Tabs, Form Controls) instead of reusing this file-level aggregate directly.