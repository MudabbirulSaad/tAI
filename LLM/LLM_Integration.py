from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
from LLM.prompt import promptTemplate
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class llm():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash"

    class Command(BaseModel):
        command: str

    def generate_command(self, query: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=promptTemplate,
                response_mime_type="application/json",
                response_schema=self.Command,
            ),
        )
        command_json = response.text
        command_data = json.loads(command_json)
        command = command_data["command"]
        return command