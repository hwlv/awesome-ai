import re
import sys
from typing import Optional, Union, Tuple, Dict
from dotenv import load_dotenv
from openai_compatible_client import OpenAICompatibleClient
from query_weather import get_weather
from search_attraction import get_attraction
from system_prompt import AGENT_SYSTEM_PROMPT

# 加载环境变量
load_dotenv()

DEFAULT_USER_PROMPT = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
MAX_STEPS = 5


def build_llm_client() -> OpenAICompatibleClient:
    """初始化 LLM 客户端，参数由开发环境 .env 自动注入"""
    return OpenAICompatibleClient()


def get_user_prompt() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return DEFAULT_USER_PROMPT


def extract_action_block(llm_output: str) -> str:
    match = re.search(
        r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
        llm_output,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    return llm_output.strip()


def parse_action(action_text: str) -> Union[Tuple[str, Dict[str, str]], Tuple[None, None]]:
    tool_match = re.search(r"(\w+)\((.*)\)", action_text)
    if not tool_match:
        return None, None

    tool_name = tool_match.group(1)
    args_str = tool_match.group(2)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
    return tool_name, kwargs


def main() -> None:
    llm = build_llm_client()
    user_prompt = get_user_prompt()
    prompt_history = [f"用户请求: {user_prompt}"]

    available_tools = {
        "get_weather": get_weather,
        "get_attraction": get_attraction,
    }

    print("system_prompt", AGENT_SYSTEM_PROMPT)
    print(f"用户输入: {user_prompt}\n" + "=" * 40)

    for step in range(MAX_STEPS):
        print(f"--- 循环 {step + 1} ---\n")

        full_prompt = "\n".join(prompt_history)
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
        llm_output = extract_action_block(llm_output)

        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = (
                "错误: 未能解析到 Action 字段。请确保回复严格遵循 "
                "'Thought: ... Action: ...' 的格式。"
            )
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "=" * 40)
            prompt_history.append(observation_str)
            continue

        action_str = action_match.group(1).strip()

        if action_str.startswith("Finish"):
            finish_match = re.match(r"Finish\[(.*)\]", action_str)
            final_answer = finish_match.group(1) if finish_match else action_str
            print(f"任务完成，最终答案: {final_answer}")
            return

        tool_name, kwargs = parse_action(action_str)
        if not tool_name:
            observation = f"错误: 无法解析 Action `{action_str}`"
        elif tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)

    print("达到最大循环次数，任务未完成。")


if __name__ == "__main__":
    main()
