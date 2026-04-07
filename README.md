# Awesome AI

一个面向长期积累的个人 AI 知识库仓库。

这里不只是放链接或工具清单，而是把常用概念、skills、agent 学习笔记、参考资料和最小 demo 代码沉淀成可以持续复习的文档站点。

## 在线文档

- GitHub Pages 发布后地址: [https://hwlv.github.io/awesome-ai/](https://hwlv.github.io/awesome-ai/)

## 当前结构

```text
.
├─ docs/                     # VitePress 文档站点
│  ├─ .vitepress/           # 站点配置与主题
│  ├─ guide/                # 使用说明与路线图
│  ├─ learning/             # 学习路线与阶段实践
│  ├─ fundamentals/         # AI 基础概念
│  ├─ skills/               # Skill 与提示词模板
│  ├─ agents/               # Agent 方法与工程化
│  ├─ references/           # 参考资料
│  ├─ reviews/              # 复盘模板
│  └─ templates/            # 通用模板
├─ examples/                # 最小示例代码
├─ .github/workflows/       # GitHub Actions 部署流程
├─ package.json             # 文档与示例脚本
└─ README.md
```

## 文档栏目

- `guide`: 站点说明、阅读顺序、路线图
- `learning`: 面向 Web 开发者的 AI 学习路线与阶段实践
- `fundamentals`: AI 基本概念、prompt、RAG、tool calling
- `skills`: 常用 skill 与提示词模板
- `agents`: agent 基础与常见模式
- `references`: 精选参考资料
- `reviews`: 每周复盘
- `templates`: 可直接复用的知识模板

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
cd examples/travel-agent
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

- 按主题继续补充文档内容
- 给每个核心主题补至少一个最小示例
- 每周更新一次复盘，持续查缺补漏
