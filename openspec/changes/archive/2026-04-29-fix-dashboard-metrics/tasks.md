## 1. 后端：API 计费增量累加

- [x] 1.1 修改 `backend/routers/stats.py` 的 `get_billing_summary` 中 API 模式计算逻辑：查询 provider 所有带 balance 的 CollectionLog（按时间升序），遍历相邻两条，累加 `prev - curr` 当 `prev > curr`，跳过 `prev < curr`（充值）
- [x] 1.2 手动验证：启动后端，对一个 API 模式的 provider 确认 billing-summary 接口返回正确的增量累加金额

## 2. 前端：Pill 预设重构

- [x] 2.1 修改 `frontend/src/views/BalanceView.vue` 的 `presets` 数组为 3 个 pill：当天（1d window, 1h bucket）、7天（7d window, ~5.76h bucket 按线性缩放）、30天（30d window, 24h bucket）
- [x] 2.2 修改 `activePreset` 默认值为 1（7天 pill）
- [x] 2.3 更新 `buildConsumption` bucket 逻辑以适配新的 bucket 值（现有逻辑无需大改，bucket 值来自 presets 配置）

## 3. 前端：图表渲染修正

- [x] 3.1 修改 `renderChart` 的 series padding：每条折线独立锚定，起点为 `firstBucket - bMs` 处 y=0，终点为 `lastBucket + bMs` 处 y=0（不再使用窗口边界）
- [x] 3.2 修改 `renderChart` 的 yAxis 配置：设置 `min: 0`，不设置 `max`（自动缩放）
- [x] 3.3 修改 `renderChart` 的 xAxis 配置：`min`/`max` 由所有 series 的起止 bucket 范围决定（`min = min(firstBucket) - bMs`, `max = max(lastBucket) + bMs`）
- [x] 3.4 确认 Y 轴上限随数据自动缩放，下限固定为 0

## 4. 验证

- [x] 4.1 在浏览器中依次切换 3 个 pill，确认每个 pill 都有图表产出
- [x] 4.2 确认折线从 y=0 起点连接到第一个聚合点，再经过所有点到最后一个聚合点，最后回到 y=0
- [x] 4.3 确认 X 轴右端对齐到 bucket 边界（如 1h bucket 下当前 14:35 → max=15:00）
- [x] 4.4 确认费用卡片在 API 模式 provider 有充值记录后仍然显示正确的累计消耗金额
