# 构建模块

这一层回答的是：

- Prompt 在系统里到底控制什么
- Tool Calling 什么时候值得上
- RAG 和长上下文分别解决什么问题

这里不是在讨论完整系统，而是在拆系统最常见的三个能力块。

## 本栏包含什么

1. [Prompt 基础](/components/prompting)
2. [Embeddings 与 RAG](/components/embeddings-rag)
3. [Tool Calling](/components/tool-calling)

## 和上一层、下一层的边界

- `foundations/` 负责建立概念地图
- `components/` 负责拆能力模块
- `systems/` 负责把多个模块组合成 workflow 或 agent
