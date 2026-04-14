# 知识地图与目录结构

这次重构的目标，不是单纯把栏目换个名字，而是把仓库改成一套更稳定的分层：

1. 学习者先知道“先学什么，后学什么”。
2. 再知道“AI 系统由哪些层组成”。
3. 最后把文档、代码、模板、资料放到各自稳定的位置。

## 顶层分类

| 栏目 | 回答的问题 | 对应目录 |
| --- | --- | --- |
| 开始 | 这个仓库怎么用 | `docs/guide/` |
| 学习路径 | 先学什么、每阶段产出什么 | `docs/learning/` |
| 核心原理 | AI 应用到底由什么组成 | `docs/foundations/` |
| 构建模块 | Prompt、RAG、Tool Calling 这些能力块怎么工作 | `docs/components/` |
| 系统设计 | 怎么把模块拼成 workflow / agent / 工程系统 | `docs/systems/` |
| 实战项目 | 哪些代码可以直接跑，分别在说明什么 | `docs/practice/` + `examples/` |
| 资料库 | 模板、资料、复盘、阅读笔记 | `docs/resources/` |

这里最重要的变化是：

- `skill` 不再和 `agent` 并列。
- `demo / 示例` 不再和“概念栏目”并列。
- `agent` 被放回更高一层的“系统设计”，因为它本质上建立在 prompt、tool calling、状态管理之上。

## 仓库目录分层

```text
docs/
├─ guide/                  # 仓库使用方式、知识地图、路线图
├─ learning/               # 学习路线与阶段任务
├─ foundations/            # 核心原理与基础概念
├─ components/             # Prompt / RAG / Tool Calling 等构建模块
├─ systems/                # Agent、系统设计、工程化
├─ practice/               # 实战总览页
├─ resources/              # 资料、模板、playbooks、复盘
└─ archive/                # 暂不进入主导航的旧笔记

examples/
├─ foundations/            # 最小原理示例
├─ components/             # 单个能力模块示例
├─ systems/                # Agent / system 级示例
└─ learning/               # 按阶段组织的学习项目
```

## 放内容时怎么判断位置

- 解释“是什么 / 为什么重要”放 `foundations/`
- 解释“一个能力模块怎么工作”放 `components/`
- 解释“多个模块怎么协作成系统”放 `systems/`
- 可运行代码放 `examples/`
- 阶段任务、验收标准、学习计划放 `learning/`
- 模板、复盘、资料卡片、提示词资产放 `resources/`

## 为什么这样更稳

- 它把“知识层级”和“工程目录”对齐了。
- 它避免把术语当栏目名，减少后续继续膨胀。
- 它允许你以后继续扩展 `memory`、`evals`、`workflow`、`case studies`，而不用再推倒重来。
