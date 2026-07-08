"""
Question Factory OS
OpenAI Provider
"""

import os

from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError
from openai import AuthenticationError
from openai import APIConnectionError

from core.config_manager import ConfigManager

load_dotenv()


class OpenAIProvider:

    def __init__(self):

        self.config = ConfigManager().load()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.responses.create(
                model=self.config["model"],
                input=prompt
            )

            return response.output_text

        except AuthenticationError:
            raise RuntimeError(
                "OpenAI authentication failed. Check your API key."
            )

        except RateLimitError:
            raise RuntimeError(
                "OpenAI quota exceeded. Check your API billing and usage."
            )

        except APIConnectionError:
            raise RuntimeError(
                "Unable to connect to OpenAI."
            )

        except Exception as ex:
            raise RuntimeError(
                f"OpenAI Error: {ex}"
            )
            
                 