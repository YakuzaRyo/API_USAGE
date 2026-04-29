## Context

两个独立 bug 影响系统可用性，需同时修复。

### Bug 1: Backend startup

`main.py` 被修改为依赖 Alembic 迁移，但无 `alembic.ini` 和迁移文件。`init_db()` 被删除。数据库表不创建，旧数据库文件可能缺新列。

### Bug 2: Frontend freeze

`JsonPathTagCloud.vue` 用 `h()` 在 `v-for` 中渲染 VNode。每次 Vue 重渲染调用 `rootNodes()` 同步创建全部 VNode 树，JSON 嵌套深或节点多时卡死主线程。

## Goals / Non-Goals

**Goals:**
- 恢复 `init_db()` 确保数据库表自动创建
- JsonPathTagCloud 改为纯 Vue 模板递归组件

**Non-Goals:**
- 不设置 Alembic（后续单独处理）
- 不改变 JsonPathTagCloud 的 props/emits 接口

## Decisions

### 1. Backend: 恢复 `init_db()`

```python
# lifespan 启动时
await init_db()  # 恢复原调用
```

移除 Alembic 导入和 `_run_migrations` 线程。`init_db()` 使用 `Base.metadata.create_all` 创建所有表。

### 2. Frontend: 递归模板组件

```vue
<!-- JsonTreeLeaf.vue — 递归组件 -->
<template>
  <div v-if="isLeaf">{{ key }}: {{ formatValue }}</div>
  <div v-else>
    <div @click="toggle">{{ expanded ? '▼' : '▶' }} {{ key }}</div>
    <div v-if="expanded" v-for="(child, ck) in children" :key="ck">
      <JsonTreeLeaf :node="child" :depth="depth + 1" @select="..." />
    </div>
  </div>
</template>
```

Vue 3 `<script setup>` 中组件文件名自动注册，递归自引用无需 `import`。

## Risks / Trade-offs

- `init_db()` 使用 `create_all`，不处理已有表的列变更。若 Schema 添加了新列但表已存在，`create_all` 不会自动 ALTER TABLE。→ 开发阶段可删除 `*.db` 重置；生产需用 Alembic。
- 递归组件模板比 `h()` 慢（多了一层组件实例），但远快于卡死的同步 VNode 创建。

## Open Questions

- 无。
