## 1. JsonPathTagCloud 重写

- [x] 1.1 重写 `JsonPathTagCloud.vue`：组件改为递归 JSON 树渲染，每个节点显示 key + 类型感知的 value
- [x] 1.2 实现折叠/展开：对象和数组节点显示三角 toggle，默认展开 depth < 2，点击切换状态
- [x] 1.3 点击任意 key → `emit('select', { path })`（保持现有接口不变）
- [x] 1.4 实现长字符串截断（>30 字符 `...` + title 完整显示）+ 数组超过 20 元素截断
- [x] 1.5 实现原始 JSON toggle（`<details>/<summary>` 折叠，默认隐藏）
- [x] 1.6 树节点缩进每层 16px，hover 高亮当前行，样式与项目风格一致

## 2. ProviderWizard 输入框改造

- [x] 2.1 Step 2：删除 `<pre>` 原始 JSON 块；Token 总量/费用输入框改为 tag-container 形式
- [x] 2.2 Step 3：删除 `<pre>` 原始 JSON 块；余额输入框改为 tag-container 形式
- [x] 2.3 Tag-container：点击聚焦（触发 onInputFocus），× 删除清空，placeholder 提示"点击 JSON 树中的 key 填入路径"
- [x] 2.4 验证 tag-container 的聚焦态橙色边框保留

## 3. 验证

- [x] 3.1 验证 JSON 树默认展开 2 层、折叠/展开正常
- [x] 3.2 验证点击树 key → 填入 tag → × 删除 tag 完整流程
- [x] 3.3 验证原始 JSON toggle 正常、长字符串截断正确
