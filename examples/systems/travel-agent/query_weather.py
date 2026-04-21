"""
天气查询工具模块

作为 Agent 的外部工具之一，负责查询指定城市的实时天气信息。
使用 wttr.in 免费天气 API，无需注册或 API Key。

在 ReAct Agent 中，LLM 通过输出 Action: get_weather(city="北京")
来触发本模块的调用，返回的天气信息会作为 Observation 反馈给 LLM。
"""

import requests


def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气。

    调用 wttr.in API 获取 JSON 格式的天气数据，
    提取当前天气描述和温度，返回可读的中文摘要。

    Args:
        city: 城市名称（支持中文，如"北京"、"上海"）

    Returns:
        格式化的天气信息字符串，例如: "北京当前天气:Sunny，气温28摄氏度"
        查询失败时返回以"错误:"开头的提示信息
    """
    # wttr.in 的 JSON 格式接口，format=j1 返回结构化天气数据
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        # 如果 HTTP 状态码不是 2xx，抛出异常
        response.raise_for_status()
        data = response.json()

        # 从返回的 JSON 中提取当前天气状况
        # 数据结构: { "current_condition": [{ "weatherDesc": [{"value": "..."}], "temp_C": "..." }] }
        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]["value"]  # 天气描述（如 Sunny、Cloudy）
        temp_c = current_condition["temp_C"]                        # 摄氏温度

        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"

    except requests.exceptions.RequestException as exc:
        # 网络层错误：连接超时、DNS 解析失败等
        return f"错误:查询天气时遇到网络问题 - {exc}"
    except (KeyError, IndexError) as exc:
        # 数据解析错误：API 返回格式不符合预期（可能是城市名无效）
        return f"错误:解析天气数据失败，可能是城市名称无效 - {exc}"


# 支持直接运行本模块进行快速测试
if __name__ == "__main__":
    print(get_weather("北京"))
