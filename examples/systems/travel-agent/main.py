"""
旅行助手 Agent —— 主入口模块

本模块实现了一个基于 ReAct（Reasoning + Acting）模式的 AI Agent。
核心流程：
  1. 接收用户的自然语言请求（如"查北京天气并推荐景点"）
  2. 将请求发送给大语言模型（LLM），LLM 按照 Thought → Action 格式输出推理与行动
  3. 解析 LLM 输出中的 Action，调用对应的外部工具（天气查询 / 景点搜索）
  4. 将工具返回的 Observation 追加到对话历史，再次交给 LLM 继续推理
  5. 循环执行，直到 LLM 输出 Finish[最终答案] 或达到最大循环次数

这就是经典的 "Agent Loop"（代理循环），是构建 AI Agent 的核心设计模式。
"""

import re
import sys
from typing import Optional, Union, Tuple, Dict
from dotenv import load_dotenv
from openai_compatible_client import OpenAICompatibleClient
from query_weather import get_weather
from search_attraction import get_attraction
from system_prompt import AGENT_SYSTEM_PROMPT

# 从 .env 文件加载环境变量（如 API Key、模型 ID 等）
load_dotenv()

# 默认用户提示语，当命令行未传入参数时使用
DEFAULT_USER_PROMPT = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"

# Agent 循环的最大步数，防止无限循环
MAX_STEPS = 5


def build_llm_client() -> OpenAICompatibleClient:
    """
    初始化 LLM 客户端。

    连接参数（模型名称、API Key、Base URL）由 .env 文件自动注入，
    无需在代码中硬编码敏感信息。
    """
    return OpenAICompatibleClient()


def get_user_prompt() -> str:
    """
    获取用户输入的提示语。

    优先使用命令行参数（支持多个词拼接），
    如果没有传入参数则使用 DEFAULT_USER_PROMPT 作为默认值。

    用法示例:
        python main.py 帮我查上海的天气
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return DEFAULT_USER_PROMPT


def extract_action_block(llm_output: str) -> str:
    """
    从 LLM 的完整输出中提取第一组 Thought + Action 块。

    LLM 有时会一次性输出多组 Thought/Action/Observation，
    但 Agent 每轮只应执行一个 Action，因此需要截取第一组。

    正则匹配逻辑：
      - 从 "Thought:" 开始，贪婪匹配到 "Action: ..." 的内容
      - 遇到下一个 Thought/Action/Observation 或字符串末尾时停止

    Args:
        llm_output: LLM 返回的原始文本

    Returns:
        提取出的第一组 Thought + Action 文本块
    """
    match = re.search(
        r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
        llm_output,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    return llm_output.strip()


def parse_action(action_text: str) -> Union[Tuple[str, Dict[str, str]], Tuple[None, None]]:
    """
    解析 Action 字符串，提取工具名称和关键字参数。

    期望的 Action 格式: function_name(arg1="value1", arg2="value2")

    例如:
        输入: 'get_weather(city="北京")'
        输出: ('get_weather', {'city': '北京'})

    Args:
        action_text: Action 行的文本内容

    Returns:
        (tool_name, kwargs) 元组；解析失败时返回 (None, None)
    """
    # 匹配函数调用格式: 函数名(参数列表)
    tool_match = re.search(r"(\w+)\((.*)\)", action_text)
    if not tool_match:
        return None, None

    tool_name = tool_match.group(1)       # 工具/函数名称
    args_str = tool_match.group(2)        # 括号内的参数字符串

    # 提取所有 key="value" 形式的关键字参数，构建字典
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
    return tool_name, kwargs


def main() -> None:
    """
    Agent 主循环 —— ReAct 模式的核心实现。

    执行流程:
      1. 构建 LLM 客户端和工具注册表
      2. 将用户请求加入 prompt 历史
      3. 进入循环：
         a. 拼接完整 prompt 历史，调用 LLM 获取推理结果
         b. 从 LLM 输出中解析 Action
         c. 如果 Action 是 Finish → 输出最终答案并退出
         d. 如果 Action 是工具调用 → 执行工具，获取 Observation
         e. 将 Observation 追加到 prompt 历史，进入下一轮循环
      4. 超过 MAX_STEPS 仍未完成则提示超时
    """
    # ---- 初始化 ----
    llm = build_llm_client()
    user_prompt = get_user_prompt()

    # prompt_history 是整个 Agent 的"记忆"，
    # 每轮循环都会追加 LLM 输出和工具返回的 Observation，
    # 下一轮会把完整历史拼接后发给 LLM，让它了解之前发生了什么。
    prompt_history = [f"用户请求: {user_prompt}"]

    # 工具注册表：将工具名称映射到实际的 Python 函数
    # Agent 通过字符串匹配来决定调用哪个工具
    available_tools = {
        "get_weather": get_weather,        # 天气查询工具
        "get_attraction": get_attraction,  # 景点推荐工具
    }

    print("system_prompt", AGENT_SYSTEM_PROMPT)
    print(f"用户输入: {user_prompt}\n" + "=" * 40)

    # ---- Agent 循环（最多 MAX_STEPS 轮） ----
    for step in range(MAX_STEPS):
        print(f"--- 循环 {step + 1} ---\n")

        # 将所有历史记录拼接为一个完整的 prompt，发送给 LLM
        full_prompt = "\n".join(prompt_history)
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)

        # 提取第一组 Thought + Action（防止 LLM 一次输出多步）
        llm_output = extract_action_block(llm_output)

        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        # ---- 解析 Action ----
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            # LLM 输出格式不符合预期，提示它修正
            observation = (
                "错误: 未能解析到 Action 字段。请确保回复严格遵循 "
                "'Thought: ... Action: ...' 的格式。"
            )
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "=" * 40)
            prompt_history.append(observation_str)
            continue

        action_str = action_match.group(1).strip()

        # ---- 判断是否为终止动作 ----
        if action_str.startswith("Finish"):
            # Finish[最终答案] 表示 Agent 认为任务已完成
            finish_match = re.match(r"Finish\[(.*)\]", action_str)
            final_answer = finish_match.group(1) if finish_match else action_str
            print(f"任务完成，最终答案: {final_answer}")
            return

        # ---- 执行工具调用 ----
        tool_name, kwargs = parse_action(action_str)
        if not tool_name:
            # Action 格式无法解析为函数调用
            observation = f"错误: 无法解析 Action `{action_str}`"
        elif tool_name in available_tools:
            # 通过工具注册表动态调用对应函数，并传入解析出的参数
            observation = available_tools[tool_name](**kwargs)
        else:
            # LLM 试图调用一个不存在的工具
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 将工具执行结果作为 Observation 追加到历史，供下一轮 LLM 参考
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)

    # 超过最大循环次数仍未输出 Finish，提示用户
    print("达到最大循环次数，任务未完成。")


if __name__ == "__main__":
    main()
