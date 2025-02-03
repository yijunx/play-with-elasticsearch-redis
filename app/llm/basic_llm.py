from typing import Iterable

from openai import Client


class MessageForLLM:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def model_dump(self):
        return {"role": self.role, "content": self.content}


class BasicLLM:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model
        self.client = Client(base_url=self.base_url, api_key=self.api_key)

    def stream_response(
        self,
        conversation: list[MessageForLLM],
        sys_prompt: str,
        temperature: int,
        frequency_penalty: float = None,
    ) -> Iterable[str]:
        messages = [
            {
                "role": "system",
                "content": sys_prompt,
            },
        ] + [x.model_dump() for x in conversation]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            stream=True,
        )
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                yield chunk_message

    def full_response(
        self,
        conversation: list[MessageForLLM],
        sys_prompt: str,
        temperature: int,
        frequency_penalty: float = None,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": sys_prompt,
            },
        ] + [x.model_dump() for x in conversation]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
        )
        return response.choices[0].message.content

    def get_response(
        self,
        sys_prompt: str = None,
        user_prompt: str = None,
        temperature: int = 0,
        frequency_penalty: float = None,
    ) -> str:

        if not sys_prompt and not user_prompt:
            raise ValueError(
                "At least one of sys_prompt or user_prompt must be provided"
            )

        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
        )
        return response.choices[0].message.content
