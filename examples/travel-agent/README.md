# Travel Agent

这个示例来自 `ai-study/agent-study/1`，已经按当前仓库结构重新整理过。

它和 `examples/simple-agent` 的区别是：

- `simple-agent`：不依赖真实模型和外部工具，只演示最小循环结构
- `travel-agent`：接入真实 LLM、天气查询和搜索工具，演示一个更接近实战的单 agent 工具调用流程

## 目录结构

```text
examples/travel-agent/
├─ main.py
├─ openai_compatible_client.py
├─ query_weather.py
├─ search_attraction.py
├─ system_prompt.py
└─ requirements.txt
```

## 依赖

建议先创建虚拟环境，再安装：

```bash
cd examples/travel-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 环境变量

运行前至少需要准备：

```bash
export LLM_API_KEY="your-llm-api-key"
export LLM_MODEL="deepseek-chat"
export LLM_BASE_URL="https://api.deepseek.com"
export TAVILY_API_KEY="your-tavily-api-key"
```

说明：

- `LLM_API_KEY`：兼容 OpenAI 接口的模型服务凭证
- `LLM_MODEL`：模型 ID
- `LLM_BASE_URL`：兼容 OpenAI 接口的服务地址
- `TAVILY_API_KEY`：Tavily 搜索服务密钥

如果你使用的是 OpenAI 官方接口，也可以只设置：

```bash
export OPENAI_API_KEY="your-openai-key"
export LLM_MODEL="gpt-4.1-mini"
```

## 运行

默认会执行这个学习用任务：

- 查询北京天气
- 根据天气推荐合适景点

直接运行：

```bash
python main.py
```

也可以传入自定义请求：

```bash
python main.py "帮我查询今天上海的天气，并推荐一个适合散步的景点"
```

## 这个示例适合学什么

- system prompt 如何约束 Thought / Action 输出
- agent loop 如何维护 `prompt_history`
- 工具调用如何从模型文本中解析出来
- 外部工具失败时如何把错误回传给模型继续决策

## 局限

- 这里仍然是教学示例，不是生产级 agent
- 工具解析基于正则，格式稍微漂移就可能失败
- 没有 memory、plan、retry policy、structured output 等更稳的机制
