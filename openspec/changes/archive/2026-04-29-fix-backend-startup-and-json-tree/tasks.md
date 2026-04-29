## 1. 后端修复

- [x] 1.1 `main.py`: 移除 Alembic 相关 import 和 `_run_migrations` 线程
- [x] 1.2 `main.py`: 在 lifespan 中恢复 `await init_db()` 调用
- [x] 1.3 确认 `from database import engine, init_db, AsyncSessionLocal` 导入完整

## 2. 前端修复

- [x] 2.1 新建 `JsonTreeLeaf.vue` 递归组件：接收 `nodeKey` + `value` + `path` + `depth` props，emit `select`
- [x] 2.2 重写 `JsonPathTagCloud.vue`：移除 `h()` 和 `rootNodes()`，改用 `<JsonTreeLeaf>` 模板递归
- [x] 2.3 保留折叠/展开、默认展开 depth < 1（即根节点展开 1 层）、长字符串截断、原始 JSON toggle
- [x] 2.4 验证点击测试 API 不卡死

## 3. 验证

- [x] 3.1 启动后端无报错，`GET /api/providers` 正常返回
- [x] 3.2 删除 `*.db` 后重启，表自动创建
- [x] 3.3 点击测试按钮前端不卡死
