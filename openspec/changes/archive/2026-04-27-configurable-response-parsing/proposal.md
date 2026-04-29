## Why

不同 LLM 厂商的 API 响应格式各异（OpenAI、DeepSeek、Anthropic 结构都不同），硬编码解析器无法覆盖。需要改为用户可配置的 JSONPath 映射，让用户通过"测试 API→查看原始响应→配置提取路径"的方式自行适配任意厂商格式。同时余额需要支持配置货币符号。

## What Changes

- 删除硬编码的 OpenAI/Anthropic 格式解析器，改为纯 JSONPath（点号路径）驱动
- Provider 模型：`response_mapping` 拆为 `usage_mapping` + `balance_mapping`，新增 `currency_symbol`
- test endpoint 改为返回原始 JSON 响应，方便用户查看后配置映射
- 前端 Provider 表单新增"测试 API"按钮和映射路径配置输入框
- 前端 Dashboard 余额卡牌使用 `currency_symbol` 替代硬编码 CNY

## Capabilities

### New Capabilities

- `configurable-response-mapping`: 用户可配置 JSONPath 映射来解析用量和余额响应，测试 API 返回原始 JSON 辅助配置

### Modified Capabilities

无。

## Impact

后端：
- `backend/models.py` — response_mapping → usage_mapping + balance_mapping + currency_symbol
- `backend/routers/providers.py` — Schema 更新，test 返回原始 JSON
- `backend/services/collector.py` — 删除硬编码解析，纯 mapping 驱动

前端：
- `frontend/src/api/index.ts` — Provider 类型更新
- `frontend/src/views/ProviderView.vue` — 测试按钮 + mapping 配置 UI
- `frontend/src/views/DashboardView.vue` — currency_symbol
