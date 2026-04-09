"""
阶段 4 - 完整的 AI 问答后端
包含：对话管理、流式输出、健康检查
"""

import os
import json
import uuid
import time
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ============================================================
# 配置
# ============================================================
app = FastAPI(
    title="AI 问答助手 API",
    description="一个面向 Web 开发者的 AI 问答服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================
# 数据模型
# ============================================================
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[str] = None
    system_prompt: str = "你是一个有帮助的AI助手，擅长回答编程和AI相关的问题。"
    stream: bool = False

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    timestamp: str
    latency_ms: float

class Message(BaseModel):
    role: str
    content: str
    timestamp: str

# ============================================================
# 对话存储（生产环境应使用 Redis/数据库）
# ============================================================
conversations: dict[str, list[Message]] = {}

# ============================================================
# LLM 服务（可替换为真实 API 调用）
# ============================================================
def generate_reply(messages: list[dict], system_prompt: str) -> str:
    """
    生成回复 - 当前使用模拟实现
    实际使用时替换为:

    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + messages,
    )
    return response.choices[0].message.content
    """
    user_msg = messages[-1]["content"] if messages else ""

    # 模拟一些智能回复
    responses = {
        "你好": "你好！我是 AI 助手，有什么可以帮你的吗？",
        "hello": "Hello! I'm an AI assistant. How can I help you?",
    }

    for key, reply in responses.items():
        if key in user_msg.lower():
            return reply

    return (
        f"收到你的问题：「{user_msg}」\n\n"
        f"这是一个模拟回复。在实际部署中，这里会调用 OpenAI/本地模型来生成回答。\n\n"
        f"要启用真实 AI 回复：\n"
        f"1. 设置环境变量 `OPENAI_API_KEY`\n"
        f"2. 取消 generate_reply 函数中的真实 API 调用注释"
    )

def generate_reply_stream(messages: list[dict], system_prompt: str):
    """流式生成回复"""
    reply = generate_reply(messages, system_prompt)
    for char in reply:
        time.sleep(0.02)  # 模拟逐字生成
        yield char

# ============================================================
# API 端点
# ============================================================
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """非流式对话接口"""
    start = time.time()

    conv_id = request.conversation_id or str(uuid.uuid4())
    if conv_id not in conversations:
        conversations[conv_id] = []

    # 记录用户消息
    user_msg = Message(
        role="user",
        content=request.message,
        timestamp=datetime.now().isoformat()
    )
    conversations[conv_id].append(user_msg)

    # 构建消息列表
    messages = [{"role": m.role, "content": m.content}
                for m in conversations[conv_id][-20:]]

    # 生成回复
    reply = generate_reply(messages, request.system_prompt)

    # 记录助手消息
    assistant_msg = Message(
        role="assistant",
        content=reply,
        timestamp=datetime.now().isoformat()
    )
    conversations[conv_id].append(assistant_msg)

    latency = (time.time() - start) * 1000

    logger.info(f"Chat | conv={conv_id[:8]} | latency={latency:.0f}ms | "
                f"input_len={len(request.message)} | output_len={len(reply)}")

    return ChatResponse(
        reply=reply,
        conversation_id=conv_id,
        timestamp=datetime.now().isoformat(),
        latency_ms=round(latency, 2)
    )


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式对话接口 (Server-Sent Events)"""
    conv_id = request.conversation_id or str(uuid.uuid4())
    if conv_id not in conversations:
        conversations[conv_id] = []

    conversations[conv_id].append(Message(
        role="user",
        content=request.message,
        timestamp=datetime.now().isoformat()
    ))

    messages = [{"role": m.role, "content": m.content}
                for m in conversations[conv_id][-20:]]

    async def event_generator():
        full_reply = ""
        for token in generate_reply_stream(messages, request.system_prompt):
            full_reply += token
            data = json.dumps({"token": token, "done": False}, ensure_ascii=False)
            yield f"data: {data}\n\n"

        # 保存完整回复
        conversations[conv_id].append(Message(
            role="assistant",
            content=full_reply,
            timestamp=datetime.now().isoformat()
        ))

        yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Conversation-Id": conv_id}
    )


@app.get("/api/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    """获取对话历史"""
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {
        "conversation_id": conv_id,
        "messages": [m.model_dump() for m in conversations[conv_id]],
        "message_count": len(conversations[conv_id])
    }


@app.get("/api/conversations")
async def list_conversations():
    """列出所有对话"""
    return {
        "conversations": [
            {
                "id": conv_id,
                "message_count": len(msgs),
                "last_message": msgs[-1].content[:100] if msgs else ""
            }
            for conv_id, msgs in conversations.items()
        ],
        "total": len(conversations)
    }


@app.delete("/api/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    """删除对话"""
    if conv_id in conversations:
        del conversations[conv_id]
    return {"status": "deleted", "conversation_id": conv_id}


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "active_conversations": len(conversations),
        "total_messages": sum(len(msgs) for msgs in conversations.values()),
        "api_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "timestamp": datetime.now().isoformat()
    }

# ============================================================
# 启动说明
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 启动 AI 问答服务...")
    print("📖 API 文档: http://localhost:8000/docs")
    print("❤️  健康检查: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
