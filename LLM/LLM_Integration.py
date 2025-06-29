from litellm import completion
import litellm
from dotenv import load_dotenv
import json
import os
from LLM.prompt import promptTemplate
from pydantic import BaseModel

# Load environment variables
load_dotenv()
litellm.enable_json_schema_validation = True


class llm:
    def __init__(self):
        # self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini/gemini-2.0-flash"

    class Command(BaseModel):
        command: str

    def generate_command(self, model: str, query: str) -> str:
        messages = [
            {"role": "system", "content": promptTemplate},
            {"role": "user", "content": query},
        ]
        response = completion(
            model=model,
            messages=messages,
            api_key=os.getenv("GEMINI_API_KEY"),
            response_format=self.Command,
        )
        response_json = json.loads(response.model_dump()['choices'][0]['message']['content'])
        command = response_json['command']
        return command