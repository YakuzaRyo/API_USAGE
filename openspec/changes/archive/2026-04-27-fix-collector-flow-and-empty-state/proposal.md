## Why

Collector 在 usage API 失败时直接 return，导致已配置的 balance API 始终不被查询。前端厂商管理页空状态有两个"新增厂商"按钮，样式冗余。

## What Changes

- 后端 collector：usage 和 balance 采集解耦，互不阻塞，各自独立记录 CollectionLog
- 前端空状态：删除空状态中的重复按钮，改为虚线边框可点击卡片，仅在无厂商时展示

## Capabilities

### New Capabilities

无。这是对已实现系统的缺陷修复。

### Modified Capabilities

无。

## Impact

- `backend/services/collector.py` — usage 失败不再 return，继续执行 balance 采集
- `frontend/src/views/ProviderView.vue` — 空状态改为虚线框卡片
- `frontend/src/style.css` — 新增 `.empty-add` 虚线框样式
