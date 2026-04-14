# 实战项目

这个栏目对应仓库根目录下的 `examples/`。这里不再把所有 demo 平铺，而是按“学习层级”组织代码。

## 目录分层

### 1. Foundations

- 目录：`examples/foundations/prompt-basics`
- 作用：演示最小 prompt 结构应该包含哪些部分

### 2. Components

- 目录：`examples/components/tool-calling`
- 作用：演示工具注册、工具选择、执行与结果回传的基本循环

- 目录：`examples/components/rag-lite`
- 作用：用一个极简检索脚本解释“先召回，再生成”的思路

### 3. Systems

- 目录：`examples/systems/simple-agent`
- 作用：演示最小 agent loop 如何管理目标、行动和停止条件

- 目录：`examples/systems/travel-agent`
- 作用：演示一个接入真实模型服务、天气查询和搜索工具的 Python agent 示例
- 适合对比看：先看 `simple-agent` 理解循环骨架，再看这个示例理解“模型 + 工具 + 观察结果”如何真正串起来

### 4. Learning Stages

- 目录：`examples/learning/stage-1-python-math`
- 目录：`examples/learning/stage-2-classical-ml`
- 目录：`examples/learning/stage-3-deep-learning`
- 目录：`examples/learning/stage-4-ai-web-product`
- 作用：配合学习路径使用，每个阶段都有对应的交付物和练习代码

## 建议的使用方式

1. 先读对应主题文档。
2. 再跑同层级里的最小示例。
3. 最后自己改一处参数、规则或数据，确认理解是否真正落地。
