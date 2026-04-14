# 学习路径总览

这组内容来自 `ai-study` 里的学习路线和阶段任务，但已经按当前仓库的结构重新组织过。

这里不回答"概念是什么"，而是回答另外一类问题：

- 先学什么，后学什么
- 每个阶段要做出什么交付物
- 配套代码和复盘应该放在哪

## 为什么单独拆成 `learning`

当前站点已经有比较清晰的分工：

- `foundations`：解释核心概念和技术边界
- `components`：拆 Prompt、RAG、Tool Calling 这类构建模块
- `systems`：记录 agent 设计、模式和工程化方法
- `practice`：汇总真正可运行的最小示例
- `resources`：放模板、复盘、资料卡和 playbooks

而 `ai-study` 里的核心价值，是一条面向 Web 开发者的学习路线和阶段实践计划。它和 `foundations` 不是一类内容，硬塞进去会让栏目职责变混。

## 当前仓库里的推荐落位

- `docs/learning/`：路线图、阶段目标、任务清单、验收标准
- `examples/learning/`：每个阶段的配套可运行代码
- `docs/resources/reviews/`：每周复盘、阶段复盘
- `docs/resources/templates/`：知识卡片、项目总结、PRD 模板

配套代码按阶段组织：

```text
examples/learning/
├─ stage-1-python-math/     # Python 语法、NumPy、数学概念
│  ├─ scripts/              # 4 个可运行脚本
│  └─ notebooks/
├─ stage-2-classical-ml/    # Titanic 建模全流程
│  ├─ src/                  # 数据探索 + 模型对比
│  └─ models/
├─ stage-3-deep-learning/   # PyTorch 训练流程
│  ├─ src/                  # Tensor 基础 + MNIST 分类
│  └─ models/
└─ stage-4-ai-web-product/  # AI 问答产品
   ├─ backend/              # FastAPI 后端
   └─ frontend/             # 问答界面
```

这样文档和代码的边界会比较清楚：

- 学习说明、任务清单放 `docs/learning`
- 真的能跑的脚本或项目放 `examples/learning/`
- 其他模块性知识分别回到 `foundations / components / systems / resources`

## 推荐阅读顺序

1. [Web 开发者转 AI 学习路线](/learning/web-developer-to-ai-roadmap) — 总体路线、周计划、自我评估
2. [阶段 1：Python 与数学基础](/learning/python-math-basics) — 环境搭建、语法对比、数学代码验证
3. [阶段 2：经典机器学习](/learning/classical-ml) — Titanic 全流程、Pipeline、模型对比
4. [阶段 3：深度学习核心](/learning/deep-learning-core) — PyTorch 训练、CNN/LSTM、模型部署
5. [阶段 4：AI + Web 产品化](/learning/ai-web-product) — LLM 集成、RAG、Agent、前端界面

每个阶段都包含：阶段目标、核心任务（附带完整代码）、推荐资料、交付物清单和完成标准。

## 怎么和现有栏目配合看

- 看不懂概念时，回到 [核心原理](/foundations/)
- 要理解 Prompt、RAG、Tool Calling，回到 [构建模块](/components/)
- 要做 agent、自动化或工程化时，回到 [系统设计](/systems/)
- 要整理模板或复盘方式时，回到 [资料库](/resources/)
- 要验证理解是否落地，去看 [实战项目](/practice/)
