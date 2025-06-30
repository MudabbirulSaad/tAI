provider = "openrouter/deepseek/deepseek-chat:free"

print(provider.split('/')[0])

import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("GEMINI_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("ANTHROPIC_API_KEY"))
print(os.getenv("OPENROUTER_API_KEY"))