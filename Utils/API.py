import os
from dotenv import load_dotenv

load_dotenv(override=True)

def get_api_key(model:str) -> str:

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