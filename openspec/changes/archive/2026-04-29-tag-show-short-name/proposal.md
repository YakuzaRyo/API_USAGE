## Why

映射输入框中的路径 tag 显示完整 JSONPath（`balance_infos.0.total_balance`），对用户来说冗余且难读。用户只需要看到最后一段 key 名（`total_balance`）即可确认选择正确。

## What Changes

- `ProviderWizard.vue`: 3 处 mapping-tag 文字从完整路径改为 `.split('.').pop()`

## Capabilities

### New Capabilities
- `tag-show-short-name`: Mapping path tags display only the leaf key name instead of the full dot-path

## Impact

- [ProviderWizard.vue](frontend/src/components/ProviderWizard.vue) — 3 行模板改动
