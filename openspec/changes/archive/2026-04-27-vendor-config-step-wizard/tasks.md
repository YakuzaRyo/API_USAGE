## 1. JsonPathTagCloud 组件

- [x] 1.1 创建 `frontend/src/components/JsonPathTagCloud.vue`，接收 `json: unknown` prop
- [x] 1.2 实现 `parseLeafPaths()` 递归解析函数，提取叶子节点路径（string/number/boolean/null），按深度排序，限制 50 条
- [x] 1.3 渲染 tag 列表（flex-wrap 布局），点击 tag 时 emit `select` 事件 `{ path: string }`
- [x] 1.4 Tag 悬停态样式（hover 过渡到 --color-primary 背景 + 白色文字）及空态/截断提示

## 2. ProviderWizard — 基础结构 + Step 1

- [x] 2.1 创建 `frontend/src/components/ProviderWizard.vue`，组件接收 `provider?: Provider` prop 和 `@close` emit
- [x] 2.2 实现 Modal 壳体（overlay + content，关闭按钮，点击 overlay 关闭）
- [x] 2.3 实现 `currentStep` ref (1|2|3) 和表单状态（reactive，所有字段的初始值从 provider 填充或默认值）
- [x] 2.4 实现 Step 1 表单：名称、API Key（password）、Base URL、追踪模型（tag add/remove），含必填校验与行内错误提示
- [x] 2.5 实现 Step 1 的「保存并继续」按钮逻辑：校验 → 组装 payload → POST（新建）或 PUT（编辑）→ `currentStep = 2`

## 3. ProviderWizard — Step 2 用量路径

- [x] 3.1 实现 Step 2 表单：Usage API Path 输入框 +「测试」按钮，调用 `testApi`
- [x] 3.2 测试成功后展示 JSON 响应（pre 块，最大高度滚动），并用 `<JsonPathTagCloud>` 渲染 tag
- [x] 3.3 实现映射输入框聚焦跟踪（`focusedTarget` ref, @focus 设置, @blur 延迟 200ms 清除）
- [x] 3.4 Tag 点击时根据 `focusedTarget` 填入对应输入框（tokens → usage_mapping_total_tokens, cost → usage_mapping_cost），无聚焦时显示提示
- [x] 3.5 映射输入框聚焦态橙色边框样式（`:focus` + `box-shadow: 0 0 0 2px var(--color-primary)`）

## 4. ProviderWizard — Step 3 余额 & 其他

- [x] 4.1 实现 Step 3 表单：Balance API Path +「测试」按钮 + JSON 响应 + Tag 云（复用 Step 2 模式）
- [x] 4.2 Tag 点击填入余额映射输入框（`focusedTarget === 'balance'`）
- [x] 4.3 实现货币符号（input，默认 "CNY"）和轮询间隔（select，默认 300，复用现有 intervalOptions）
- [x] 4.4 实现 Step 3「保存」按钮：组装完整 payload → PUT/POST → emit close 事件关闭 wizard

## 5. 导航系统

- [x] 5.1 实现圆点导航器：3 个圆点水平居中，当前步放大（20px 填充色），其余缩小（12px 空心），点击跳转
- [x] 5.2 实现「上一步」按钮（Step 2/3 显示，Step 1 隐藏），点击 currentStep--
- [x] 5.3 Step 切换时保持表单状态不丢失（所有字段在 reactive 中跨步持久）

## 6. ProviderView 集成

- [x] 6.1 在 ProviderView.vue 中引入 `<ProviderWizard>` 替换原 Modal 内的单页表单
- [x] 6.2 适配 openCreate / openEdit 逻辑，传递 provider prop 和监听 @close 事件
- [x] 6.3 移除 ProviderView.vue 中不再需要的旧表单代码（form、formErrors、testResult、testing 等 local state）
- [x] 6.4 验证新建 → Step 1 保存 → 列表刷新 → 再次编辑增量填充的完整流程
