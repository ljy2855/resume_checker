# clients/ollama_client.py
import requests
import json
from django.conf import settings
from clients import BaseClient


class OllamaClient(BaseClient):
    def __init__(self):
        self.base_url = settings.OLLAMA_API_ENDPOINT

    def evaluate_text(self, text):
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "model": "llama3",
            "stream": False,
            "prompt": "You evaluate the developer application and correct the problematic parts in the application.\n"
            + text,
        }
        response = requests.post(self.base_url, json=data)
        print(response.text)
        response_data = response.json()
        if response.status_code == 200:

            return response_data.get("response", "")
        else:
            raise Exception(
                f"API Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
            )
