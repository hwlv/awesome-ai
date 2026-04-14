# Examples

这里放和文档配套的最小示例代码。

## 当前目录

- `foundations/prompt-basics`: 最小 prompt 结构示例
- `components/tool-calling`: 工具调用循环示例
- `components/rag-lite`: 极简检索示例
- `systems/simple-agent`: 极简 agent loop 示例
- `systems/travel-agent`: 接入真实天气和搜索工具的 Python agent 示例
- `learning/`: 按学习阶段组织的配套项目

## 运行方式

在仓库根目录执行：

```bash
npm run example:prompt
npm run example:tools
npm run example:rag
npm run example:agent
```

这些脚本都不依赖外部模型服务，重点是帮助理解结构和流程。

如果要运行 `travel-agent`，请进入对应目录按 Python 方式安装依赖并配置环境变量：

```bash
cd examples/systems/travel-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
