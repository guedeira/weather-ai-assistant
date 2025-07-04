# src/clients/openai_client.py
from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS

    def create_chat_completion(self, messages, tools=None, tool_choice=None):
        """
        Creates a chat completion with the OpenAI API, handling function calls.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response
        except Exception as e:
            print(f"An error occurred with OpenAI API: {e}")
            return None