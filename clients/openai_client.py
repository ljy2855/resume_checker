# clients/openai_client.py
import openai
from django.conf import settings

from clients import BaseClient


class OpenAIClient(BaseClient):
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def evaluate_text(self, text):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an interviewer who picks a developer and please rate the resume",
                },
                {
                    "role": "system",
                    "content": "Correct the problems in the application.",
                },
                {"role": "user", "content": "hello"},
            ],
        )
        return response.choices[0].message["content"]
