import os
from typing import Optional, Union
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()


class OpenAICompatibleClient:
    """
    为 Awesome AI 定制的 LLM 客户端，参考 Hello-Agents 风格实现。
    封装了 OpenAI 兼容接口的调用，支持环境变量加载和流式/非流式响应。
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
    ):
        # 优先使用传入参数，否则从环境变量读取
        self.model = model or os.getenv("LLM_MODEL_ID") or os.getenv("LLM_MODEL")
        api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")

        if not all([self.model, api_key]):
            raise ValueError(
                "❌ 错误: 模型 ID 或 API 密钥未提供，且未在环境变量或 .env 中定义。"
            )

        client_kwargs = {"api_key": api_key, "timeout": timeout}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用大语言模型生成响应"""
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
            answer = response.choices[0].message.content
            print("✅ 大语言模型响应成功。")
            return answer or ""
        except Exception as exc:
            print(f"❌ 调用 LLM API 时发生错误: {exc}")
            return "错误:调用语言模型服务时出错。"
