# Awesome AI

一个面向长期积累的个人 AI 学习仓库。

这里不只是放链接或工具清单，而是把学习路径、核心原理、构建模块、系统设计、实战代码和资料模板沉淀成可以持续复习的文档站点。

## 在线文档

- GitHub Pages 发布后地址: [https://hwlv.github.io/awesome-ai/](https://hwlv.github.io/awesome-ai/)

## 当前结构

```text
.
├─ docs/                     # VitePress 文档站点
│  ├─ .vitepress/           # 站点配置与主题
│  ├─ guide/                # 使用说明、知识地图、路线图
│  ├─ learning/             # 学习路线与阶段实践
│  ├─ foundations/          # AI 核心原理与概念地图
│  ├─ components/           # Prompt / RAG / Tool Calling 等模块
│  ├─ systems/              # Agent、系统设计、工程化
│  ├─ practice/             # 实战总览页
│  ├─ resources/            # 资料、模板、playbooks、复盘
│  └─ archive/              # 暂不进入主导航的旧笔记
├─ examples/                # 按层级组织的可运行代码
│  ├─ foundations/          # 原理级最小示例
│  ├─ components/           # 模块级最小示例
│  ├─ systems/              # Agent / system 级示例
│  └─ learning/             # 各阶段配套项目
├─ .github/workflows/       # GitHub Actions 部署流程
├─ package.json             # 文档与示例脚本
└─ README.md
```

## 文档栏目

- `guide`: 站点说明、知识地图、阅读顺序
- `learning`: 面向 Web 开发者的 AI 学习路线与阶段实践
- `foundations`: AI 基本概念与模型接入基础
- `components`: Prompt、RAG、Tool Calling 等构建模块
- `systems`: Agent 基础、模式与工程化
- `practice`: 实战项目总览
- `resources`: 参考资料、playbooks、复盘和模板

## 本地使用

安装依赖：

```bash
npm install
```

启动文档站点：

```bash
npm run docs:dev
```

构建文档：

```bash
npm run docs:build
```

运行最小示例：

```bash
npm run example:prompt
npm run example:tools
npm run example:rag
npm run example:agent
```

额外还有一个 Python 版 agent 示例：

```bash
cd examples/systems/travel-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## GitHub Pages 自动部署

仓库已经配置了 GitHub Actions 工作流。要让站点正常发布，请在 GitHub 仓库设置里确认：

1. 打开 `Settings -> Pages`
2. `Source` 选择 `GitHub Actions`
3. 推送到 `main` 后，工作流会自动构建并发布站点

## 后续建议

- 继续沿着 `foundations -> components -> systems -> practice` 扩内容
- 给每个核心主题补至少一个最小示例
- 每周更新一次复盘，持续查缺补漏
