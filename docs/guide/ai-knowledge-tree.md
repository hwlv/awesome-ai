# AI 知识树（建议版）

这份文档不是要一次写完全部内容，而是先把“AI 词汇应该放在哪一层”固定下来。

你的站点继续保留这 6 个顶层栏目：

- `learning`：学习顺序
- `foundations`：概念基础
- `components`：能力模块
- `systems`：系统搭建
- `practice`：实战项目
- `resources`：资料库

其中最容易混淆的，是 `foundations / components / systems`。可以先记一句话：

- `foundations`：解释“这是什么”
- `components`：解释“这个能力怎么用”
- `systems`：解释“多个能力怎么拼成系统”

## 一套更细的目录草案

下面这棵树是建议版，你后续可以按它慢慢补文档，不需要一次建完。

```text
docs/
├─ guide/
│  ├─ start-here.md
│  ├─ knowledge-architecture.md
│  ├─ ai-knowledge-tree.md
│  └─ site-roadmap.md
├─ learning/
│  ├─ index.md
│  ├─ web-developer-to-ai-roadmap.md
│  ├─ python-math-basics.md
│  ├─ classical-ml.md
│  ├─ deep-learning-core.md
│  └─ ai-web-product.md
├─ foundations/
│  ├─ index.md
│  ├─ ai-basics.md
│  ├─ ai-ml-dl-llm-relationship.md
│  ├─ transformer-basics.md
│  ├─ tokens-and-context-window.md
│  ├─ inference-vs-training.md
│  ├─ pretraining-sft-rlhf.md
│  ├─ fine-tuning-basics.md
│  ├─ reasoning-and-hallucination.md
│  ├─ multimodal-basics.md
│  ├─ evaluation-basics.md
│  └─ model-api-access.md
├─ components/
│  ├─ index.md
│  ├─ prompting.md
│  ├─ context-engineering.md
│  ├─ structured-output.md
│  ├─ embeddings.md
│  ├─ chunking-and-retrieval.md
│  ├─ reranking.md
│  ├─ embeddings-rag.md
│  ├─ knowledge-base-design.md
│  ├─ tool-calling.md
│  ├─ mcp-and-tool-protocols.md
│  ├─ memory-basics.md
│  └─ multimodal-io.md
├─ systems/
│  ├─ index.md
│  ├─ workflow-basics.md
│  ├─ agent-basics.md
│  ├─ agent-patterns.md
│  ├─ planning-and-decomposition.md
│  ├─ reflection-and-self-correction.md
│  ├─ state-and-memory-architecture.md
│  ├─ multi-agent-collaboration.md
│  ├─ guardrails-and-safety.md
│  ├─ evals-and-observability.md
│  ├─ cost-latency-reliability.md
│  ├─ llmops.md
│  ├─ harness-engineering.md
│  └─ agent-first-engineering.md
├─ practice/
│  ├─ index.md
│  ├─ prompt-playground.md
│  ├─ rag-lite.md
│  ├─ tool-agent.md
│  ├─ knowledge-chatbot.md
│  └─ coding-agent.md
└─ resources/
   ├─ index.md
   ├─ glossary/
   │  └─ ai-glossary.md
   ├─ landscape/
   │  ├─ model-vendors.md
   │  ├─ agent-frameworks.md
   │  ├─ vector-databases.md
   │  └─ ai-product-patterns.md
   ├─ playbooks/
   ├─ reading-notes/
   ├─ reviews/
   └─ templates/
```

## 各层到底放什么

### 1. `foundations` 概念基础

这一层放“相对稳定”的东西，重点是建立脑子里的地图。

建议子主题：

- AI、ML、DL、LLM 之间是什么关系
- Transformer 是什么
- Token、上下文窗口、采样、大模型推理在说什么
- 训练、推理、预训练、SFT、RLHF 分别是什么
- 微调到底解决什么，不解决什么
- 推理能力、幻觉、能力边界
- 多模态模型基础
- 评估到底在评什么

常见词汇归类：

- `Transformer`：放这里
- `Token` / `Context Window`：放这里
- `Pretraining / SFT / RLHF`：放这里
- `Fine-tuning`：先放这里
- `Hallucination`：放这里
- `Reasoning`：放这里

### 2. `components` 能力模块

这一层放“单个能力块”，重点是搞清楚每个模块独立解决什么问题。

建议子主题：

- Prompt 基础与提示结构
- Context Engineering
- Structured Output / JSON 模式
- Embedding
- Chunking
- Retrieval
- Reranking
- RAG
- Knowledge Base 设计
- Tool Calling
- MCP / 工具协议
- 多模态输入输出
- 基础记忆机制

常见词汇归类：

- `Prompt Engineering`：放这里
- `Context Engineering`：放这里
- `Structured Output`：放这里
- `Embedding`：放这里
- `Chunking`：放这里
- `Retrieval`：放这里
- `Rerank / Reranking`：放这里
- `RAG`：放这里
- `Tool Calling / Function Calling`：放这里
- `MCP`：先放这里
- `Memory`：如果讲单个记忆能力，先放这里

### 3. `systems` 系统搭建

这一层放“组合关系”和“工程问题”，重点不是一个词本身，而是它如何在系统里协作。

建议子主题：

- Workflow 和 Agent 的区别
- 单 Agent 设计
- 多 Agent 协作
- Planning / Decomposition
- Reflection / Self-correction
- 状态管理与长期记忆架构
- Guardrails / 安全边界
- Evals / 观测 / 追踪
- 成本、延迟、稳定性
- LLMOps
- Harness Engineering
- Agent First Engineering

常见词汇归类：

- `Workflow`：放这里
- `Agent`：放这里
- `Planning`：放这里
- `Reflection`：放这里
- `Multi-Agent`：放这里
- `State Management`：放这里
- `Long-term Memory`：放这里
- `Guardrails`：放这里
- `Evals`：放这里
- `Observability`：放这里
- `Harness Engineering`：放这里
- `LLMOps`：放这里

## 你提到的几个词，建议这样放

| 词 | 建议位置 | 理由 |
| --- | --- | --- |
| RAG | `components` | 它本质上是检索增强这个能力模块 |
| Embedding | `components` | 它是 RAG 的底层能力块之一 |
| Chunking | `components` | 它属于检索链路里的拆分策略 |
| Reranking | `components` | 它属于检索排序能力 |
| Context Engineering | `components` | 它是“如何构造输入上下文”的能力设计 |
| Prompt Engineering | `components` | 它是最基础的单点能力模块 |
| Tool Calling | `components` | 它先是能力接口，再进入系统编排 |
| MCP | `components` | 先把它当工具接入协议理解最稳 |
| Agent | `systems` | 它不是单个能力，而是多个模块的组合体 |
| Workflow | `systems` | 它是系统组织方式 |
| Memory | `components` 或 `systems` | 讲单个记忆能力放前者，讲长期记忆架构放后者 |
| Harness Engineering | `systems` | 它是智能体时代的工程方法，不是单模块知识 |
| Evals | `systems` | 它关心的是整个系统是否稳定可控 |
| Guardrails | `systems` | 它关心系统边界，不是单点能力 |

## 一个很实用的判断规则

当你遇到一个新词时，可以按这三个问题判断它放哪：

1. 它是在解释基础概念吗？
   是的话，放 `foundations`
2. 它是在解释某个单点能力怎么工作吗？
   是的话，放 `components`
3. 它是在解释多个能力怎么组合、约束、评估、落地吗？
   是的话，放 `systems`

## 后续推荐补充顺序

如果你想系统学 AI，不建议按流行词一个个追。更稳的补法是：

1. 先补 `foundations`：把概念地图搭起来
2. 再补 `components`：把 Prompt、RAG、Tool Calling、Context Engineering 补齐
3. 再补 `systems`：把 Agent、Workflow、Evals、Harness Engineering 补齐
4. 最后用 `practice` 和 `resources` 做落地与复盘

## 最后一个建议

不要把所有词都变成顶层栏目。

更稳的做法是：

- 顶层只保留少量稳定分类
- 热门词、新术语、新框架都先挂到二级或三级主题下
- 只有当一类内容长期膨胀时，才考虑升级为独立专题

这样你的知识库不会因为 AI 圈的新词太多而不断重构。
