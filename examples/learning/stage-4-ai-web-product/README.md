# 阶段 4：AI + Web 产品化 - 配套代码

## 环境准备

```bash
cd backend
pip install fastapi uvicorn openai pydantic python-dotenv
```

## 文件说明

| 文件 | 内容 | 运行方式 |
|-----|------|---------|
| `backend/app.py` | 完整 AI 问答后端 | `uvicorn backend.app:app --reload` |
| `frontend/index.html` | 问答界面 | 浏览器直接打开 |

## 快速开始

```bash
# 1. 设置 API Key
export OPENAI_API_KEY="your-key-here"

# 2. 启动后端
cd backend && uvicorn app:app --reload --port 8000

# 3. 打开前端
open frontend/index.html
```

## 产品架构

```
用户 → 前端界面 → FastAPI 后端 → LLM API
                      ↓
                  日志/监控
```
