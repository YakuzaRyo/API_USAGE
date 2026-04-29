## Context

当前 JsonPathTagCloud 将 JSON 解析为扁平叶子节点路径列表并以 inline tag 展示。ProviderWizard Step 2/3 同时展示原始 JSON `<pre>` 块和 tag 云。用户反馈展示形式不直观。

## Goals / Non-Goals

**Goals:**
- JSON 树形视图：递归缩进，折叠/展开，默认展开前 2 层
- 点击任意 key → emit `select { path }`（与现有接口一致）
- 输入框改为 tag-container 形式：点击 key 后以 tag 填入，可 × 删除
- 原始 JSON 折叠 toggle，默认隐藏
- 长字符串截断（>30 字符），hover 显示完整
- 不改动 emits 接口（仍用 `select { path: string }`）

**Non-Goals:**
- 不改变 JsonPathTagCloud 的 props/emits 接口签名
- 不改变 onTagSelect 逻辑

## Decisions

### 1. 组件结构

JsonPathTagCloud.vue 内部递归渲染 JSON 节点。每个节点类型：

```typescript
interface TreeNode {
  key: string      // 当前 key 名（root 为 ""）
  value: unknown
  path: string     // 从 root 到当前节点的完整 JSONPath
  depth: number
  expanded: boolean  // 默认 depth < 2
}
```

组件内部用 `<div v-for>` 递归渲染子节点，不需要单独的 TreeNode 组件文件。

### 2. 节点渲染

```
▼ [key]          ← 对象/数组：三角 + key + value 预览
  ▼ [child]      ← 子节点缩进 16px/depth
    key: "val"    ← 叶子节点：key + value（灰色，截断 >30 字符）
    key: 123
    key: null
```

- **折叠/展开**：点击三角图标或 key 名
- **emit path**：点击任意 key 区域 → `emit('select', { path })`
- **数组**：key 显示为 `[0]`、`[1]` 带灰色括号
- **value 截断**：叶子节点 value 超过 30 字符 → `value.slice(0, 30) + '...'`，title 属性显示完整值

### 3. 原始 JSON toggle

```html
<details>
  <summary>查看原始 JSON</summary>
  <pre>{{ JSON.stringify(json, null, 2) }}</pre>
</details>
```

使用原生的 `<details>/<summary>` 标签，零 JS 逻辑。

### 4. 输入框改造为 tag-container

ProviderWizard 中的映射输入框从 `<input>` 改为一个**可点击的 tag-container**：

```html
<!-- 将原来的 input -->
<input v-model="form.usage_mapping_total_tokens" class="mapping-input" ... />

<!-- 改为 -->
<div class="mapping-tag-container" @click="onInputFocus('tokens')">
  <span v-if="form.usage_mapping_total_tokens" class="mapping-tag">
    {{ form.usage_mapping_total_tokens }}
    <span class="tag-remove" @click.stop="form.usage_mapping_total_tokens = ''">&times;</span>
  </span>
  <span v-else class="mapping-placeholder">点击 JSON 树中的 key 填入路径</span>
</div>
```

- 容器本身可点击聚焦（用于 onInputFocus）
- tag 显示 path 文本，带 × 删除按钮
- 删除后恢复为 placeholder 文字
- 样式与 `.tag` 一致

### 5. 保持聚焦机制不变

`focusedTarget`、`onInputFocus`、`onInputBlur`、`onTagSelect` 逻辑完全不变。唯一变化：`onTagSelect` 设置的是 `form.xxx` 值（字符串），但渲染时以 tag 形式展示。

## Risks / Trade-offs

- **深层嵌套 JSON**：默认只展开前 2 层，深层折叠避免 UI 膨胀。
- **数组大量元素**：每个数组元素独立渲染一行，数组超过 20 个元素时截断显示，加"显示更多"。
- **emits 接口不变**：外部组件无感知。

## Open Questions

- 无。Explore 阶段已充分确认。
