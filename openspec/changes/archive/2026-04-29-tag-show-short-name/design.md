## Context

ProviderWizard 中 mapping-tag 显示完整 JSONPath。改为只显示 leaf key。

## Decisions

```vue
<!-- Before -->
{{ form.usage_mapping_total_tokens }}

<!-- After -->
{{ form.usage_mapping_total_tokens.split('.').pop() }}
```

3 处 tag 同改。后端提交值不变（仍是完整路径）。
