# Tool Calling

这个示例用最小代码解释 tool calling 的基本循环：

1. 注册工具
2. 让模型决定要不要调用工具
3. 执行工具
4. 把结果回传

这里没有接真实模型，而是用一个极简 planner 来模拟决策。

## 运行

```bash
npm run example:tools
```
