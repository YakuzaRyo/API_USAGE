## Why

1. `main.py` 原有的 `await init_db()` 被替换为未配置的 Alembic 迁移调用。`alembic.ini` 和 `alembic/` 迁移目录不存在，导致线程静默崩溃，数据库表从未创建。旧数据库文件残留的表结构能支撑部分端点，但新增列（如 `CollectionLog.balance`）会导致查询异常，表现为后端不响应请求。
2. `JsonPathTagCloud.vue` 使用 `h()` 渲染函数在 `<template>` 的 `v-for` 中渲染 VNode，这种混合用法导致每次 Vue 重渲染时大量同步 VNode 创建，重 JSON 响应会卡死主线程。

## What Changes

- `main.py`: 恢复 `await init_db()` 调用，移除未配置的 Alembic 迁移线程
- `JsonPathTagCloud.vue`: 将 `h()` 渲染函数 + `v-for` 混用改为纯 Vue `<template>` 递归组件

## Capabilities

### New Capabilities
- `fix-backend-startup`: 恢复数据库表自动创建，确保后端正常启动
- `json-tree-render-fix`: 修复 JSON 树渲染为纯模板递归组件，消除前端卡死

### Modified Capabilities
<!-- 无 -->

## Impact

- [main.py](backend/main.py) — 移除 Alembic 线程，恢复 `init_db()`
- [JsonPathTagCloud.vue](frontend/src/components/JsonPathTagCloud.vue) — 重写渲染部分为递归模板组件
