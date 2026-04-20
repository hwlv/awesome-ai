import requests


def get_weather(city: str) -> str:
    """Query the wttr.in API and return a readable weather summary."""
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # print("weather data", data)

        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        temp_c = current_condition["temp_C"]

        # # print 换行
        # print("\n")
        # print("weather_desc", weather_desc)
        # print("\n")
        # print("temp_c", temp_c)
        # print("\n")
        # print("current_condition", current_condition)
        # print("\n")
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as exc:
        return f"错误:查询天气时遇到网络问题 - {exc}"
    except (KeyError, IndexError) as exc:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {exc}"


if __name__ == "__main__":
    print(get_weather("北京"))