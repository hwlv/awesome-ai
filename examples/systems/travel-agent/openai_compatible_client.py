from openai import OpenAI


class OpenAICompatibleClient:
    """A tiny wrapper around chat completions for OpenAI-compatible APIs."""

    def __init__(self, model: str, api_key: str, base_url: str | None = None):
        self.model = model
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    def generate(self, prompt: str, system_prompt: str) -> str:
        print("正在调用大语言模型...")
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
            print("大语言模型响应成功。")
            return answer or ""
        except Exception as exc:
            print(f"调用 LLM API 时发生错误: {exc}")
            return "错误:调用语言模型服务时出错。"
