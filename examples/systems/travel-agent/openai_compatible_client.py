"""
OpenAI 兼容客户端模块

封装了对 OpenAI 兼容 API 的调用逻辑。
"OpenAI 兼容"意味着不仅支持 OpenAI 官方 API，
还支持任何遵循相同接口规范的第三方服务（如 DeepSeek、通义千问、Ollama 等），
只需修改 base_url 和 api_key 即可切换不同的 LLM 提供商。

配置优先级：构造函数参数 > 环境变量 > 报错
"""

import os
from typing import Optional, Union
from openai import OpenAI
from dotenv import load_dotenv

# 从 .env 文件加载环境变量（如 LLM_API_KEY、LLM_BASE_URL 等）
load_dotenv()


class OpenAICompatibleClient:
    """
    通用 LLM 客户端，基于 OpenAI SDK 实现。

    支持通过环境变量或构造参数配置：
      - LLM_MODEL_ID / LLM_MODEL: 模型名称（如 "gpt-4o"、"deepseek-chat"）
      - LLM_API_KEY / OPENAI_API_KEY: API 密钥
      - LLM_BASE_URL / OPENAI_BASE_URL: API 基础地址（可选，用于第三方兼容服务）
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
    ):
        """
        初始化 LLM 客户端。

        Args:
            model:    模型名称，未传入时从环境变量 LLM_MODEL_ID 或 LLM_MODEL 读取
            api_key:  API 密钥，未传入时从环境变量 LLM_API_KEY 或 OPENAI_API_KEY 读取
            base_url: API 基础地址，未传入时从环境变量读取；为 None 则使用 OpenAI 官方地址
            timeout:  请求超时时间（秒），默认 60 秒
        """
        # 优先使用传入参数，否则从环境变量读取（支持两套变量名以兼容不同配置习惯）
        self.model = model or os.getenv("LLM_MODEL_ID") or os.getenv("LLM_MODEL")
        api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")

        # 模型名称和 API 密钥是必需的，缺少则抛出异常
        if not all([self.model, api_key]):
            raise ValueError(
                "❌ 错误: 模型 ID 或 API 密钥未提供，且未在环境变量或 .env 中定义。"
            )

        # 构建 OpenAI 客户端的初始化参数
        client_kwargs = {"api_key": api_key, "timeout": timeout}
        if base_url:
            # 指定了 base_url 时，SDK 会将请求发送到该地址而非 OpenAI 官方
            client_kwargs["base_url"] = base_url

        # 创建 OpenAI SDK 客户端实例
        self.client = OpenAI(**client_kwargs)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """
        调用大语言模型生成响应。

        使用 Chat Completions API，将 system_prompt 和 user prompt 组装为消息列表，
        发送给 LLM 并返回生成的文本。

        Args:
            prompt:        用户侧的完整提示（包含历史对话上下文）
            system_prompt: 系统提示词，定义 Agent 的角色和行为规范

        Returns:
            LLM 生成的文本内容；调用失败时返回错误提示字符串
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    # system 消息：设定 Agent 的角色、可用工具和输出格式
                    {"role": "system", "content": system_prompt},
                    # user 消息：包含用户请求及之前所有的推理/观察历史
                    {"role": "user", "content": prompt},
                ],
                stream=False,  # 使用非流式模式，一次性返回完整响应
            )
            # 从响应中提取生成的文本内容
            answer = response.choices[0].message.content
            print("✅ 大语言模型响应成功。")
            return answer or ""
        except Exception as exc:
            print(f"❌ 调用 LLM API 时发生错误: {exc}")
            return "错误:调用语言模型服务时出错。"


# =============================================
# 直接运行本文件进行测试
# =============================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 OpenAICompatibleClient 测试")
    print("=" * 60)

    # ---- 测试 1: 基础对话 ----
    print("\n📌 测试 1: 基础对话（使用 .env 配置）")
    print("-" * 40)
    try:
        client = OpenAICompatibleClient()
        print(f"  ✅ 客户端创建成功，模型: {client.model}")

        result = client.generate(
            prompt="请用一句话介绍你自己。",
            system_prompt="你是一个友好的 AI 助手。"
        )
        print(f"  📝 模型回复: {result}")
    except Exception as e:
        print(f"  ❌ 测试 1 失败: {e}")

    # ---- 测试 2: 自定义 system_prompt（角色扮演） ----
    print("\n📌 测试 2: 自定义 System Prompt（角色扮演）")
    print("-" * 40)
    try:
        client = OpenAICompatibleClient()
        result = client.generate(
            prompt="Python 怎么读取 JSON 文件？",
            system_prompt="你是一位资深 Python 开发者，回答简洁，直接给出代码示例，不超过 5 行。"
        )
        print(f"  📝 模型回复:\n{result}")
    except Exception as e:
        print(f"  ❌ 测试 2 失败: {e}")

    # ---- 测试 3: 构造参数覆盖（故意传错 key 验证错误处理） ----
    print("\n📌 测试 3: 错误处理（使用无效 API Key）")
    print("-" * 40)
    try:
        bad_client = OpenAICompatibleClient(
            model="deepseek-chat",
            api_key="sk-invalid-key-for-testing",
            base_url="https://api.deepseek.com",
        )
        result = bad_client.generate(
            prompt="你好",
            system_prompt="你是助手"
        )
        print(f"  📝 返回结果: {result}")
        # 预期：不会崩溃，而是返回错误提示字符串
    except Exception as e:
        print(f"  ❌ 测试 3 异常: {e}")

    print("\n" + "=" * 60)
    print("🏁 所有测试完成！")
    print("=" * 60)
