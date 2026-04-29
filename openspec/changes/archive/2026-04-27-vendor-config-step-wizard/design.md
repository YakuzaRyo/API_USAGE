## Context

当前 [ProviderView.vue](../../../frontend/src/views/ProviderView.vue) 的编辑弹窗是一个单页表单，所有字段平铺展示。本次重构将其拆分为 3 步向导，同时新增 JSONPath Tag 云组件降低手动输入负担。项目使用 Vue 3 Composition API + Pinia + Axios，样式系统使用 CSS 自定义属性（`--color-primary: #FF6B35`，即橙色，`#E85A28` 为 hover 态），无第三方 UI 框架。

## Goals / Non-Goals

**Goals:**
- 将编辑弹窗拆分为 3 步 Step 导航，降低单页认知负担
- 实现 JSONPath Tag 云：测试响应 → 解析叶子节点 → 可点击 tag → 填入聚焦输入框
- 支持增量保存（每步独立保存，仅校验当前步字段）
- 圆点 + 按钮双导航，圆点可任意跳转

**Non-Goals:**
- 不改变后端 API 接口
- 不改变列表卡片 UI（删除、立即采集等保持原样）
- 不引入第三方 UI 库
- 不改变现有全局样式变量

## Decisions

### 1. 组件拆分

新增两个组件，均放置在 `frontend/src/components/` 下：

| 组件 | 职责 |
|------|------|
| `ProviderWizard.vue` | Step 导航、表单状态、增量保存逻辑、Modal 壳体 |
| `JsonPathTagCloud.vue` | 接收 JSON 对象 → 解析叶子节点路径 → 渲染 tag 列表 → `@select` 事件 |

ProviderView.vue 保留列表逻辑，将编辑弹窗区域替换为 `<ProviderWizard>` 调用。

**替代方案**：直接在 ProviderView.vue 内用 `<template v-if="step === 1">` 分支实现。选择组件拆分的原因：(1) ProviderView 已有 330+ 行，(2) Wizard 内部有足够复杂的状态机逻辑值得独立。

### 2. Step 状态机

```
currentStep: ref<1 | 2 | 3>(1)

导航规则:
- 圆点点击 → 直接跳转（不保存，表单数据保留在内存）
- 「保存并继续」→ 校验当前步 → 调 API 保存 → currentStep++
- 「上一步」→ 直接跳转（不保存）
- Step 3 时「保存并继续」改为「保存」，不触发跳转
- 圆点永不锁定，三个点始终可点击
```

### 3. 增量保存策略

每步保存时，将当前收集的所有表单字段组装为 payload 发送 `PUT /api/providers/:id`（编辑）或 `POST /api/providers`（新建）。

步间字段分布：

| Step | 字段 |
|------|------|
| 1 | name, api_key, base_url, models |
| 2 | usage_api_path, usage_mapping.total_tokens, usage_mapping.cost |
| 3 | balance_api_path, balance_mapping.balance, currency_symbol, interval_seconds |

Step 1 保存时校验 `{ name, api_key, base_url, models }` 非空。Step 2/3 无必填校验。

新建厂商时，首次 Step 1 保存调用 POST，返回的 `id` 存入本地状态；后续 Step 2/3 保存切换为 PUT。编辑厂商时始终 PUT。

### 4. JSONPath 解析算法

```typescript
function parseLeafPaths(obj: unknown, prefix = ''): string[] {
  if (obj === null || obj === undefined) return []
  if (typeof obj !== 'object') return [prefix] // 叶子节点
  if (Array.isArray(obj)) {
    return obj.flatMap((item, i) => parseLeafPaths(item, prefix ? `${prefix}.${i}` : `${i}`))
  }
  return Object.entries(obj as Record<string, unknown>).flatMap(
    ([key, val]) => parseLeafPaths(val, prefix ? `${prefix}.${key}` : key)
  )
}
```

叶子节点定义：值为 `string | number | boolean | null` 的节点。忽略中间对象和数组。

只解析前 50 个叶子节点，超出部分截断并显示提示「显示前 50 个路径」。

### 5. 聚焦态 & Tag 填入

输入框的聚焦态通过 CSS `:focus` 伪类 + 橙色边框实现：

```css
.mapping-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary);
}
```

（与全局 [style.css](../../../frontend/src/style.css) L122 的 `input:focus` 保持一致）

Tag 填入机制：
- 维护 `focusedTarget: ref<'tokens' | 'cost' | 'balance' | null>(null)`
- 输入框 `@focus` 设置 `focusedTarget`，`@blur` 延迟 200ms 清除（给 tag 点击留时间）
- 点击 tag → `@select` 事件 → 根据 `focusedTarget` 填入对应字段
- 若 `focusedTarget === null`，在 tag 云上方短暂显示提示「请先点击目标输入框」

### 6. 圆点导航样式

```
○        ●        ○
Step1   Step2   Step3
```

- 默认：空心圆 `○`，`12px`，边框 2px，颜色 `var(--color-border)`
- 当前：实心圆 `●`，`20px`，填充 `var(--color-primary)`
- 每个圆点可点击（`cursor: pointer`），hover 时颜色过渡到 primary
- 三个点水平居中，间距 `16px`

## Risks / Trade-offs

- **新建 → Step 1 保存后，再 Step 2 保存前的中间状态**：数据库中存在一个 models 为空、无 usage path 的半完整记录。后端已有 partial update 支持，不会报错。前端在列表中展示此类记录的模型区域会为空，属于正常行为。
- **blur/focus 竞争**：tag 点击时输入框 blur 先触发，若立即清除 `focusedTarget` 会导致 tag 点击无效。→ 使用 200ms `setTimeout` 延迟清除。
- **深层嵌套 JSON**：如果 API 返回极深的嵌套结构，叶子节点可能非常多。→ 限制展示 50 个，按路径深度排序。

## Open Questions

- 无。Explore 阶段已与用户确认所有关键交互行为。
