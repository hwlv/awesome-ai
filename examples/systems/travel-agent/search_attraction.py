"""
景点推荐工具模块

作为 Agent 的外部工具之一，负责根据城市和天气条件搜索推荐的旅游景点。
使用 Tavily Search API 进行智能搜索，需要配置 TAVILY_API_KEY 环境变量。

Tavily 是一个专为 AI Agent 设计的搜索引擎 API，
能够返回结构化的搜索结果和 AI 生成的摘要答案。
"""

import os


def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气条件，搜索推荐的旅游景点。

    通过 Tavily Search API 执行智能搜索，
    优先返回 AI 生成的摘要答案，否则返回格式化的搜索结果列表。

    Args:
        city:    城市名称（如"北京"）
        weather: 当前天气描述（如"Sunny，气温28摄氏度"），用于生成更精准的搜索查询

    Returns:
        景点推荐信息字符串；失败时返回以"错误:"开头的提示信息
    """
    # 从环境变量获取 Tavily API 密钥
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "错误:未配置 TAVILY_API_KEY 环境变量。"

    # 延迟导入 Tavily SDK —— 仅在实际调用时才检查依赖是否安装
    try:
        from tavily import TavilyClient
    except ImportError:
        return "错误:未安装 Tavily SDK，请先执行 `pip install -r requirements.txt`。"

    # 初始化 Tavily 搜索客户端
    tavily = TavilyClient(api_key=api_key)

    # 构造搜索查询：结合城市和天气信息，让搜索结果更具针对性
    query = f"'{city}' 在 '{weather}' 天气下最值得去的旅游景点推荐及理由"

    try:
        response = tavily.search(
            query=query,
            search_depth="basic",       # 搜索深度: "basic"（快速）或 "advanced"（深入）
            include_answer=True,        # 请求 Tavily 生成 AI 摘要答案
        )

        # 优先使用 Tavily 的 AI 摘要答案（更简洁、可读性更好）
        if response.get("answer"):
            return response["answer"]

        # 如果没有摘要答案，则格式化原始搜索结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")

        if not formatted_results:
            return "抱歉，没有找到相关的旅游景点推荐。"

        return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)

    except Exception as exc:
        return f"错误:执行 Tavily 搜索时出现问题 - {exc}"
