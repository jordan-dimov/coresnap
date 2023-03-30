import openai
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


@retry(
    wait=wait_random_exponential(multiplier=1, max=60),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type(
        openai.error.AuthenticationError,
    ),
)
def gpt_chat(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def gpt_outline(work_title: str):
    messages = [
        {
            "role": "system",
            "content": "The user will provide the title of a published text, such as a book, research paper, article. They may provide the name of the author as well. Generate a mindmap with the core ideas from the text and output it as an indented list of bullet points. Do not output anything else other than the indented list of bullet points. ",
        },
        {"role": "user", "content": f"Generate a mindmap of: {work_title}"},
    ]
    return gpt_chat(messages)
