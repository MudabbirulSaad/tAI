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
        # self.model = "gemini/gemini-2.0-flash"
        pass

    class Command(BaseModel):
        command: str
    
    def get_api_key(self,model:str):

        provider = model.split('/')[0]

        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                return api_key
            else:
                raise Exception("GEMINI_API_KEY is not set")
        
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                return api_key
            else:
                raise Exception("OPENAI_API_KEY is not set")
        
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                return api_key
            else:
                raise Exception("ANTHROPIC_API_KEY is not set")
            
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if api_key:
                return api_key
            else:
                raise Exception("OPENROUTER_API_KEY is not set")
            
        else:
            raise Exception("Invalid provider")

    def generate_command(self, model: str, query: str) -> str:
        messages = [
            {"role": "system", "content": promptTemplate},
            {"role": "user", "content": query},
        ]
        api_key = self.get_api_key(model)
        response = completion(
            model=model,
            messages=messages,
            api_key=api_key,
            response_format=self.Command,
        )
        response_json = json.loads(response.model_dump()['choices'][0]['message']['content'])
        command = response_json['command']
        return command