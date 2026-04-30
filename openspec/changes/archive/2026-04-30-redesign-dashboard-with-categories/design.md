## Context

当前 Provider 配置需要为同分类下每个实例重复填写 base_url / 路径 / 模型等共享字段。主看板使用 4 个矩形统计卡片 + 趋势图/分布图，无法直观展示数据分类占比。需引入 Category 模板机制和环形仪表盘，全程遵循 Neo-Brutalist 设计风格（直角、粗边框、硬阴影、`#FF6B35` 主色）。

## Goals / Non-Goals

**Goals:**
- Category CRUD 页：卡片列表 + billing_mode tab 弹窗编辑
- Provider Wizard：Step 1 顶部加 billing_mode + category 下拉，自动填充
- 主看板 pill：综合看板 / 用量分析 / 余额变化，各 pill 独立
- 综合看板：4 个 Neo-Brutalist 环形卡片，图例过滤，数据按维度占比分割
- 数据层：categories 表 + provider.category_id + stats 按 category 聚合

**Non-Goals:**
- 不修改余额变化 pill 内部实现
- 不修改用量趋势/模型分布的图表逻辑（仅搬家到新 pill）
- 不引入新的第三方图表库

## Decisions

### 1. Category 数据模型

**选择**: 独立 `categories` 表，Provider 通过 `category_id` FK 关联（可为 NULL，兼容存量数据）。

```
categories:
  id, name, api_base_url, api_usage_path, api_balance_path,
  tp_base_url, tp_usage_path, currency_symbol, models(JSON)
```

billing_mode 不同的 URL/路径分别存储在同一个 category row 的不同列中，弹窗用 tab 切换编辑。TAB 是纯前端交互，不拆分表。

### 2. 环形卡片：SVG stroke-dasharray

**选择**: 用 SVG `<circle>` + `stroke-dasharray` + `stroke-dashoffset` 实现环形占比。

```
<svg viewBox="0 0 120 120">
  <circle cx="60" cy="60" r="50" fill="none" stroke="var(--color-border)" stroke-width="10" />
  <!-- 每个 segment 一个 circle，dasharray="弧长 总周长"，dashoffset 计算偏移 -->
  <circle cx="60" cy="60" r="50" fill="none" stroke="var(--color-primary)" stroke-width="10"
          stroke-dasharray="78.5 314" stroke-dashoffset="0" />
  <!-- 中心文字用 foreignObject 或叠加的绝对定位 div -->
</svg>
```

**替代方案**: ECharts gauge — 功能强但引入新依赖且样式难定制为 Neo-Brutalist。Canvas 绘制 — 灵活性高但无障碍性差。SVG 方案最简，可直接用 CSS 变量控制颜色和描边宽度。

### 3. 双环实现

外环和内环是同一个 SVG 内的两个 `<circle>`，半径不同。外层 `r=54`，内层 `r=38`。图例分两组（外环图例、内环图例），点击外环图例同时过滤内外环对应数据。

### 4. 环形卡片 Neo-Brutalist 适配

- 卡片容器: 直角 `.card`，`box-shadow: var(--shadow-md)`，hover 浮升
- 环描边: `stroke-width="10"` 粗线，实色块无渐变
- 颜色: 首段 `--color-primary: #FF6B35`，后续段用高对比色（`#1A1A1A`, `#6B6B6B`, `#FFD23F` 等循环）
- 中心文字: `font-weight: 900`, `font-size: 28px`, 黑色
- 图例: `.tag` 风格，可点击，被过滤项加删除线

### 5. Provider Wizard 改动策略

**选择**: 保持现有 3 步结构不变，仅在 Step 1 顶部插入 billing_mode pill + category 下拉。

选中 category → 按当前 billing_mode 读取对应字段 → 填充 form。每个字段仍可手动覆盖。Step 3 去掉 billing_mode。

**替代方案**: 把 category 做成独立的第一步。未采用——增加步骤数违背"减少认知负担"原则。

### 6. 环形卡片数据聚合：客户端分组

**选择**: 不在后端 stats API 新增 `group_by` 参数，改为前端拉取全量 Provider 列表 + Categories 列表后，在 computed 中按 `category_id` 做客户端分组。

**4 个环的数据源**:

| 环 | 数据 API | 分组键 |
|---|---------|-------|
| Token 消耗 | `/stats/distribution` | model |
| 活跃厂商 | providers 列表 | category_id → name |
| 当前余额 | providers 列表 (last_balance) | 外 category_id / 内 name |
| 费用 | `/stats/billing-summary` | 外 billing_mode / 内 provider_name |

**替代方案**: 后端 `group_by` 参数。未采用——当前数据量小，客户端分组无性能问题，且避免了 stats API 的额外改造。

### 7. RingGaugeCard 组件接口

```typescript
interface RingSegment { name: string; value: number; color: string }
interface InnerSegment { name: string; value: number; color: string; outerName: string }

props: {
  title: string
  segments: RingSegment[]           // 外环（单环模式即唯一环）
  innerSegments?: InnerSegment[]    // 内环（双环模式）
  formatValue?: (v: number) => string
  totalOverride?: number            // 覆盖中心数字（双环需手动计算总合）
}
```

图例交互：点击外环项隐藏对应弧段 + 同名 outerName 的内环弧段。点击内环项仅隐藏该内环弧段。过滤后弧段比例自动重算。

### 8. 存量 Provider 无 category

综合看板中 `category_id = NULL` 的 provider 归入"未分类"弧段，文字显示为灰色。不强制要求所有 provider 绑定 category。

### 9. 启动时 migration 跳过检查

`_run_migrations()` 在每次启动时先检查当前 revision 是否已是 head，是则跳过 `command.upgrade()`，避免 SQLite 被 alembic 引擎重复锁定导致单文件数据库阻塞。

## Risks / Trade-offs

- **存量 Provider 无 category** → category_id 可为 NULL，综合看板中这些 provider 归入"未分类"弧段
- **双环 SVG 性能** → 单卡片最多 ~20 个弧段，SVG 完全够用，无性能风险
- **删除 category 后 provider 处理** → category_id 置 NULL，不级联删除
- **客户端分组随 Provider 数量增长** → 当前 ≤10 个 provider 无压力，若扩展到百级需将分组逻辑移到后端
