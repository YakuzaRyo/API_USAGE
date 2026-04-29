## 1. 后端 — 数据模型

- [x] 1.1 `backend/models.py`：response_mapping 替换为 usage_mapping (JSON) + balance_mapping (JSON) + currency_symbol (str, default "CNY")
- [x] 1.2 `backend/routers/providers.py`：Pydantic schema 更新（response_mapping → usage_mapping + balance_mapping + currency_symbol）

## 2. 后端 — 解析器重构

- [x] 2.1 `backend/services/collector.py`：删除 parse_openai_format / parse_anthropic_format，_extract_usage 和 _extract_balance 纯用 extract_value + mapping 驱动
- [x] 2.2 新增 `POST /api/providers/test-api`：临时接收 base_url/api_key/api_path，返回原始 JSON

## 3. 后端 — 统计

- [x] 3.1 `backend/routers/stats.py`：summary/trends 返回 currency_symbol

## 4. 前端

- [x] 4.1 `frontend/src/api/index.ts`：Provider 类型更新（usage_mapping / balance_mapping / currency_symbol）
- [x] 4.2 `frontend/src/views/ProviderView.vue`：表单更新（usage_mapping 字段 + balance_mapping 字段 + currency_symbol + 测试按钮 + 原始响应展示）
- [x] 4.3 `frontend/src/views/DashboardView.vue`：余额卡牌用 currency_symbol

## 5. 验证

- [x] 5.1 `npm run build` 通过
- [ ] 5.2 DeepSeek balance 能正确提取余额（需用户用真实 Key 测试）
