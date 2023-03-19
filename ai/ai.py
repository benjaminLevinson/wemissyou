import openai


def prompt(system_prompt: str, user_prompt: str, content: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
            {"role": "user", "content": content},
        ],
    )
    result = completion["choices"][0]["message"]["content"]
    return _unescape(result)


def _unescape(input: str) -> str:
    return input.encode("latin-1", "backslashreplace").decode("unicode-escape")
