from litellm import completion
import litellm
from dotenv import load_dotenv
import json
import os
from pydantic import BaseModel
from Utils.API import get_api_key
# Load environment variables
load_dotenv(override=True)
litellm.enable_json_schema_validation = True


class llm:
    def __init__(self, prompt: str):
        self.prompt = prompt

    class Command(BaseModel):
        command: str
    
    def generate_command(self, model: str, query: str) -> str:
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]
        api_key = get_api_key(model)
        response = completion(
            model=model,
            messages=messages,
            api_key=api_key,
            response_format=self.Command,
        )
        response_json = json.loads(response.model_dump()['choices'][0]['message']['content'])
        command = response_json['command']
        return command