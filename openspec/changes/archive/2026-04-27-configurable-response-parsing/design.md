## Context

将硬编码的 API 响应解析器替换为用户可配置的 JSONPath 映射。同时支持货币符号配置。

## Goals / Non-Goals

**Goals:**
- 删除 `parse_openai_format` / `parse_anthropic_format` 等硬编码解析
- 所有字段提取统一用点号路径 `extract_value(data, path)`
- test endpoint 返回原始 JSON 供用户参考配置
- 余额卡牌使用用户配置的 `currency_symbol`

**Non-Goals:**
- 不支持数组索引以外的复杂 JSONPath 语法（仅点号路径）

## Decisions

### D1: 映射字段拆分

```
旧: response_mapping = {"total_tokens": "...", "cost": "...", "balance": "..."}
新: usage_mapping  = {"total_tokens": "...", "cost": "..."}
    balance_mapping = {"balance": "..."}
```

理由：usage 和 balance 是两个独立 API，应各自配置映射。

### D2: Test endpoint 改为返回原始 JSON

`POST /api/providers/{id}/test` → `POST /api/providers/test-api`
改为接收临时参数（base_url, api_key, api_path），返回原始响应 body，不依赖已保存的 Provider。

### D3: 货币符号默认值

`currency_symbol` 默认 `"CNY"`，可在编辑时修改。Dashboard 直接使用 `provider.currency_symbol`。

### D4: 向后兼容

现有 `response_mapping` 字段的 Provider 在迁移时自动转为 `usage_mapping`。

## Risks

- 用户配置错误路径导致解析失败 → Collector 记录 error log，明确错误信息
