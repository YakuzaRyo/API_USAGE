## 1. 后端 — Collector 解耦

- [x] 1.1 `backend/services/collector.py`：usage 失败不再 return，拆为两个独立 try/except 块，各自记录 CollectionLog，balance 始终尝试

## 2. 前端 — 空状态优化

- [x] 2.1 `frontend/src/views/ProviderView.vue`：删除空状态中的重复按钮，改为虚线框可点击卡片（click → openCreate）
- [x] 2.2 `frontend/src/style.css`：新增 `.empty-add` 虚线框样式（dashed border + hover 效果）

## 3. 验证

- [x] 3.1 前端 `npm run build` TypeScript + build 通过
