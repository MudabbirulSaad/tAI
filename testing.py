# provider = "openrouter/deepseek/deepseek-chat:free"

# print(provider.split('/')[0])

import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

response = requests.get(
  url="https://openrouter.ai/api/v1/auth/key",
  headers={
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
  }
)

print(json.dumps(response.json(), indent=2))


# print(os.getenv("GEMINI_API_KEY"))
# print(os.getenv("OPENAI_API_KEY"))
# print(os.getenv("ANTHROPIC_API_KEY"))
# print(os.getenv("OPENROUTER_API_KEY"))