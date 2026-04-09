# 阶段 4：AI + Web 产品化

这是把前面三阶段真正串起来的一步。重点不再是"训练了什么模型"，而是"用户能不能稳定用起来"。

## 阶段目标

- 定义一个真实用户可用的 AI 功能或产品原型
- 建立数据、模型、接口、前端和日志的最小闭环
- 形成产品、技术和复盘文档

## Web 开发者的优势

到了这个阶段，Web 开发的经验开始变成最大的竞争力：

| 你已有的能力 | 在 AI 产品化中的用途 |
|------------|-------------------|
| 前端开发 | 构建 AI 交互界面、流式展示 |
| API 设计 | 模型服务接口、中间层编排 |
| 数据库设计 | 向量数据库、会话存储 |
| 部署运维 | 模型容器化、CI/CD |
| 用户体验 | AI 功能的交互设计 |
| 错误处理 | 模型失败时的降级策略 |

## 核心任务

### 任务 1：LLM API 集成 - 智能问答系统

```python
# llm_service.py
import os
from openai import OpenAI
from typing import Generator

# ============================
# 1. 基础 LLM 调用
# ============================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(messages: list[dict], model: str = "gpt-4o-mini") -> str:
    """基础对话调用"""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

def chat_stream(messages: list[dict], model: str = "gpt-4o-mini") -> Generator:
    """
    流式输出 —— 用户体验的关键
    类比 Web 开发：类似 Server-Sent Events (SSE)
    """
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 测试
messages = [
    {"role": "system", "content": "你是一个编程助手，回答简洁清晰。"},
    {"role": "user", "content": "用 Python 写一个快速排序"}
]

# 非流式
# response = chat(messages)
# print(response)

# 流式
# for token in chat_stream(messages):
#     print(token, end="", flush=True)

# ============================
# 2. 带上下文的对话管理
# ============================
class ConversationManager:
    """
    对话管理器
    类比 Web 开发：类似 Session 管理
    """
    def __init__(self, system_prompt: str, max_history: int = 20):
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.history: list[dict] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # 保留最近的消息，防止 token 超限
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_messages(self) -> list[dict]:
        return [
            {"role": "system", "content": self.system_prompt},
            *self.history
        ]

    def chat(self, user_input: str) -> str:
        self.add_message("user", user_input)
        response = chat(self.get_messages())
        self.add_message("assistant", response)
        return response

# 使用示例
# conv = ConversationManager("你是一个 Python 专家")
# print(conv.chat("什么是装饰器？"))
# print(conv.chat("给我一个实际的例子"))  # 模型会记住上下文
```

### 任务 2：RAG（检索增强生成）

```python
# rag_service.py
import os
import numpy as np
from openai import OpenAI
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================
# 1. 文档向量化
# ============================
def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """将文本转化为向量"""
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度"""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ============================
# 2. 简单的向量知识库
# ============================
class SimpleVectorStore:
    """
    最小向量数据库实现
    类比 Web 开发：
    - 就像一个内存缓存（Redis），但存的是向量
    - 查询不是精确匹配，而是"最相似"
    """
    def __init__(self):
        self.documents: list[dict] = []

    def add(self, text: str, metadata: Optional[dict] = None):
        """添加文档"""
        embedding = get_embedding(text)
        self.documents.append({
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        })

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """搜索最相关的文档"""
        query_embedding = get_embedding(query)
        results = []
        for doc in self.documents:
            score = cosine_similarity(query_embedding, doc["embedding"])
            results.append({
                "text": doc["text"],
                "score": score,
                "metadata": doc["metadata"]
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# ============================
# 3. RAG 问答
# ============================
class RAGService:
    """
    检索增强生成服务
    流程：用户提问 → 检索相关文档 → 拼接上下文 → LLM 生成回答
    """
    def __init__(self, vector_store: SimpleVectorStore):
        self.store = vector_store

    def answer(self, question: str, top_k: int = 3) -> dict:
        # 1. 检索
        relevant_docs = self.store.search(question, top_k=top_k)
        context = "\n\n".join([
            f"【文档{i+1}】{doc['text']}"
            for i, doc in enumerate(relevant_docs)
        ])

        # 2. 构建 Prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个知识助手。根据以下参考文档回答用户问题。\n"
                    "如果文档中没有相关信息，请坦诚说明。\n"
                    "回答时引用来源文档编号。"
                )
            },
            {
                "role": "user",
                "content": f"参考文档：\n{context}\n\n问题：{question}"
            }
        ]

        # 3. 生成回答
        answer = chat(messages)

        return {
            "answer": answer,
            "sources": [
                {"text": doc["text"][:100], "score": doc["score"]}
                for doc in relevant_docs
            ]
        }

# 使用示例
# store = SimpleVectorStore()
# store.add("PyTorch 是一个开源的深度学习框架，由 Meta 开发维护。")
# store.add("FastAPI 是一个高性能的 Python Web 框架，基于类型标注。")
# store.add("向量数据库用于存储和检索高维向量，常用于 RAG 系统。")
#
# rag = RAGService(store)
# result = rag.answer("什么是 PyTorch？")
# print(result["answer"])
```

### 任务 3：完整的 AI Web 应用

```python
# app.py - 完整的 AI 问答应用
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AI 问答助手")

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# 数据模型
# ============================
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = ""
    system_prompt: str = "你是一个有帮助的AI助手。"

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    tokens_used: int
    timestamp: str

# ============================
# 对话存储（实际项目中用 Redis 或数据库）
# ============================
conversations: dict[str, list] = {}

# ============================
# API 端点
# ============================
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """非流式对话接口"""
    conv_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"

    if conv_id not in conversations:
        conversations[conv_id] = []

    conversations[conv_id].append({
        "role": "user",
        "content": request.message
    })

    messages = [
        {"role": "system", "content": request.system_prompt},
        *conversations[conv_id][-20:]  # 最近 20 条
    ]

    # 模拟调用（实际使用时替换为真实的 LLM 调用）
    reply = f"收到你的消息：'{request.message}'。这是一个模拟回复。"

    conversations[conv_id].append({
        "role": "assistant",
        "content": reply
    })

    return ChatResponse(
        reply=reply,
        conversation_id=conv_id,
        tokens_used=len(request.message) + len(reply),
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    流式对话接口（SSE）
    类比 Web 开发：就像 WebSocket，但更简单
    前端用 EventSource 或 fetch + ReadableStream 消费
    """
    async def generate():
        reply = f"这是对 '{request.message}' 的流式回复，每个字会逐个发送。"
        for char in reply:
            data = json.dumps({"token": char, "done": False})
            yield f"data: {data}\n\n"

        yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/api/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    """获取对话历史"""
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {"conversation_id": conv_id, "messages": conversations[conv_id]}

@app.delete("/api/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    """删除对话"""
    if conv_id in conversations:
        del conversations[conv_id]
    return {"status": "deleted"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "active_conversations": len(conversations),
        "timestamp": datetime.now().isoformat()
    }

# 运行: uvicorn app:app --reload --port 8000
```

### 任务 4：前端集成

```html
<!-- index.html - AI 问答前端 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 问答助手</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            padding: 16px 24px;
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }

        .message {
            margin-bottom: 16px;
            display: flex;
            gap: 12px;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }

        .message.user .avatar {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }

        .message.assistant .avatar {
            background: linear-gradient(135deg, #11998e, #38ef7d);
        }

        .message .content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.6;
            font-size: 14px;
        }

        .message.user .content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message.assistant .content {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom-left-radius: 4px;
        }

        .input-area {
            padding: 16px 24px;
            background: rgba(255, 255, 255, 0.05);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .input-wrapper {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 12px;
        }

        .input-wrapper textarea {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            color: #e0e0e0;
            font-size: 14px;
            resize: none;
            outline: none;
            font-family: inherit;
            height: 48px;
            transition: border-color 0.2s;
        }

        .input-wrapper textarea:focus {
            border-color: #667eea;
        }

        .input-wrapper button {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-size: 14px;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
        }

        .input-wrapper button:hover {
            opacity: 0.9;
        }

        .input-wrapper button:active {
            transform: scale(0.98);
        }

        .input-wrapper button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .typing-indicator {
            display: inline-flex;
            gap: 4px;
            padding: 8px 0;
        }

        .typing-indicator span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #667eea;
            animation: typing 1.4s infinite both;
        }

        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI 问答助手</h1>
    </div>

    <div class="chat-container" id="chatContainer">
        <!-- 消息会动态插入这里 -->
    </div>

    <div class="input-area">
        <div class="input-wrapper">
            <textarea
                id="userInput"
                placeholder="输入你的问题..."
                rows="1"
            ></textarea>
            <button id="sendBtn" onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000';
        const chatContainer = document.getElementById('chatContainer');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        // 回车发送
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        function addMessage(role, content) {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.innerHTML = `
                <div class="avatar">${role === 'user' ? '👤' : '🤖'}</div>
                <div class="content">${content}</div>
            `;
            chatContainer.appendChild(div);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            return div;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            userInput.value = '';
            sendBtn.disabled = true;

            // 显示用户消息
            addMessage('user', message);

            // 显示加载状态
            const loadingDiv = addMessage('assistant',
                '<div class="typing-indicator"><span></span><span></span><span></span></div>'
            );

            try {
                // 流式请求
                const response = await fetch(`${API_BASE}/api/chat/stream`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let fullReply = '';

                loadingDiv.querySelector('.content').textContent = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const text = decoder.decode(value);
                    const lines = text.split('\n').filter(l => l.startsWith('data: '));

                    for (const line of lines) {
                        const data = JSON.parse(line.slice(6));
                        if (!data.done) {
                            fullReply += data.token;
                            loadingDiv.querySelector('.content').textContent = fullReply;
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                    }
                }
            } catch (error) {
                loadingDiv.querySelector('.content').textContent =
                    '抱歉，请求失败。请检查后端服务是否运行中。';
                console.error('请求失败:', error);
            }

            sendBtn.disabled = false;
            userInput.focus();
        }
    </script>
</body>
</html>
```

### 任务 5：Agent 设计与工具调用

```python
# agent.py - 简单的 AI Agent 实现
import os
import json
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================
# 1. 定义工具
# ============================
def search_web(query: str) -> str:
    """模拟网络搜索"""
    return f"搜索结果：关于'{query}'的信息...（这里接入真实搜索引擎）"

def calculate(expression: str) -> str:
    """安全的数学计算"""
    try:
        # 只允许数学运算
        allowed = set("0123456789+-*/().% ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"计算结果: {expression} = {result}"
        return "不支持的表达式"
    except Exception as e:
        return f"计算错误: {e}"

def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================
# 2. 工具注册表
# ============================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索网络获取信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "search_web": search_web,
    "calculate": calculate,
    "get_current_time": get_current_time
}

# ============================
# 3. Agent 核心循环
# ============================
class SimpleAgent:
    """
    一个简单的 ReAct Agent
    类比 Web 开发：就像一个中间件链
    请求 → 理解意图 → 调用工具 → 整合结果 → 返回响应
    """
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.system_prompt = """你是一个智能助手，可以使用工具来帮助回答问题。
当你需要搜索信息时，使用 search_web 工具。
当你需要计算时，使用 calculate 工具。
当你需要知道当前时间时，使用 get_current_time 工具。
请先思考是否需要使用工具，然后再回答。"""

    def run(self, user_input: str, max_steps: int = 5) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]

        for step in range(max_steps):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # 如果模型不需要调用工具，直接返回
            if not message.tool_calls:
                return message.content

            # 执行工具调用
            messages.append(message)
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"  🔧 调用工具: {func_name}({func_args})")
                result = TOOL_FUNCTIONS[func_name](**func_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return "达到最大步数限制"

# 使用示例
# agent = SimpleAgent()
# print(agent.run("今天是几号？帮我算一下 365 * 24 等于多少"))
```

### 任务 6：MLOps 最小闭环

```python
# mlops.py - 最小 MLOps 实践
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel

# ============================
# 1. 结构化日志
# ============================
class AILogger:
    """
    AI 应用日志记录器
    类比 Web 开发：类似 Morgan/Winston 中间件
    """
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger("ai_app")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(
            self.log_dir / f"{datetime.now():%Y-%m-%d}.log"
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        ))
        self.logger.addHandler(handler)

    def log_request(self, request_id: str, input_text: str,
                    output_text: str, latency_ms: float,
                    tokens_used: int, model: str):
        """记录每次 AI 请求"""
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_length": len(input_text),
            "output_length": len(output_text),
            "latency_ms": latency_ms,
            "tokens_used": tokens_used
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def log_error(self, request_id: str, error: str, context: dict):
        """记录错误"""
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context
        }
        self.logger.error(json.dumps(log_entry, ensure_ascii=False))

# ============================
# 2. 简单的 A/B 测试框架
# ============================
import hashlib

class ABTester:
    """
    简单的 A/B 测试
    类比 Web 开发：和前端的 Feature Flag 一样
    """
    def __init__(self):
        self.experiments: dict[str, dict] = {}
        self.results: dict[str, list] = {}

    def create_experiment(self, name: str, variants: dict):
        """
        创建实验
        variants: {"control": {"model": "gpt-4o-mini"},
                   "treatment": {"model": "gpt-4o"}}
        """
        self.experiments[name] = variants
        self.results[name] = []

    def get_variant(self, experiment: str, user_id: str) -> tuple[str, dict]:
        """根据用户 ID 确定分组（确保同一用户始终在同一组）"""
        variants = list(self.experiments[experiment].keys())
        hash_val = int(hashlib.md5(
            f"{experiment}:{user_id}".encode()
        ).hexdigest(), 16)
        variant_name = variants[hash_val % len(variants)]
        return variant_name, self.experiments[experiment][variant_name]

    def record_result(self, experiment: str, variant: str,
                      user_id: str, metric: float):
        """记录实验结果"""
        self.results[experiment].append({
            "variant": variant,
            "user_id": user_id,
            "metric": metric,
            "timestamp": datetime.now().isoformat()
        })

# ============================
# 3. 配置管理
# ============================
class AIConfig(BaseModel):
    """
    类比 Web 开发：就像 .env 配置文件
    但更结构化，支持不同环境的模型配置
    """
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout_seconds: int = 30
    max_retries: int = 3
    cache_ttl_seconds: int = 3600
    rate_limit_per_minute: int = 60

    # 降级策略
    fallback_model: str = "gpt-3.5-turbo"
    fallback_enabled: bool = True

    @classmethod
    def from_env(cls, env: str = "development"):
        """从环境变量加载配置"""
        configs = {
            "development": cls(
                model="gpt-4o-mini",
                temperature=0.7,
                max_retries=1
            ),
            "production": cls(
                model="gpt-4o",
                temperature=0.3,
                max_retries=3,
                rate_limit_per_minute=30
            )
        }
        return configs.get(env, cls())

# ============================
# 4. 健康检查
# ============================
class HealthChecker:
    """系统健康检查"""

    @staticmethod
    async def check_all() -> dict:
        checks = {
            "api_key": bool(os.getenv("OPENAI_API_KEY")),
            "log_dir": Path("logs").exists(),
            "disk_space_ok": True,  # 实际检测可用磁盘
            "timestamp": datetime.now().isoformat()
        }
        checks["overall"] = all([
            checks["api_key"],
            checks["log_dir"],
            checks["disk_space_ok"]
        ])
        return checks
```

## 建议实践方向

| 项目方向 | 技术栈 | 难度 |
|---------|--------|------|
| 智能 FAQ 系统 | RAG + FastAPI + React | ⭐⭐ |
| 代码审查助手 | LLM API + GitHub Webhook | ⭐⭐ |
| 文档摘要工具 | Embedding + 前端上传 | ⭐⭐ |
| 图像质检面板 | CNN + 标注界面 | ⭐⭐⭐ |
| 客服 AI Agent | Agent + 工具调用 + 知识库 | ⭐⭐⭐ |
| 多模态内容生成 | LLM + 图像生成 API | ⭐⭐⭐ |

## 建议交付物

- PRD 或功能说明
- 技术方案文档
- 可运行 Demo（前后端完整）
- API 文档和基本运维说明
- 一篇阶段复盘，说明真实问题、指标和迭代路线

## 推荐资料

| 资料 | 类型 | 说明 |
|-----|------|------|
| Made With ML 产品化章节 | 教程 | 从模型到产品 |
| Full Stack Deep Learning | 课程 | 工程化最佳实践 |
| FastAPI 官方文档 | 文档 | 后端框架 |
| OpenAI API 文档 | 文档 | LLM 接入指南 |
| 《Practical MLOps》 | 书 | MLOps 实践 |

## 配套工程建议

这一阶段最容易出现"什么都堆在一个目录里"的问题，建议从一开始就把职责拆清楚：

```text
examples/learning/stage-4-ai-web-product/
├─ README.md
├─ backend/
│  ├─ app.py              # FastAPI 主入口
│  ├─ llm_service.py      # LLM 调用封装
│  ├─ rag_service.py      # RAG 检索服务
│  ├─ agent.py            # Agent 实现
│  ├─ mlops.py            # 监控和配置
│  └─ requirements.txt
├─ frontend/
│  └─ index.html          # 前端界面
├─ data/
│  └─ knowledge_base/     # 知识库文档
├─ docs/
│  ├─ prd.md              # 产品需求
│  ├─ tech-design.md      # 技术方案
│  └─ deployment.md       # 部署说明
├─ scripts/
│  ├─ init_db.py          # 初始化脚本
│  └─ eval.py             # 评测脚本
└─ logs/
```

- `backend/`：推理服务、工作流编排、接口层
- `frontend/`：用户交互界面
- `data/`：样例知识库、种子数据、评测集
- `docs/`：PRD、技术方案、部署说明
- `scripts/`：初始化、评测、运维辅助脚本

## 常见误区

- 只关注模型表现，不关注用户体验和失败路径
- 过早堆复杂框架，但没有把日志、告警和降级方案想清楚
- 有 Demo，没有文档，过一周自己都说不清为什么这么做
- 不做成本估算，LLM 调用费用可能远超服务器成本
- 不考虑响应延迟对用户体验的影响

## 完成标准

- [ ] 产品 Demo 可以被别人按说明跑起来
- [ ] 关键流程有最小监控和错误处理
- [ ] 能说清当前版本的边界、风险和下一步改进点
- [ ] 前端能流式展示 AI 的推理结果
- [ ] 有完整的技术文档和项目复盘
