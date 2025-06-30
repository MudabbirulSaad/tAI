"""
This module handles updating API keys in the .env file.
"""
from dotenv import set_key, find_dotenv

def update_api_key(provider: str, api_key: str) -> None:
    """
    Updates the API key for a given provider in the .env file.

    Args:
        provider (str): The name of the provider (e.g., 'google', 'openai').
        api_key (str): The API key to set.
    """
    dotenv_path = find_dotenv()
    if not dotenv_path:
        # Create .env file if it doesn't exist
        with open(".env", "w") as f:
            pass
        dotenv_path = find_dotenv()

    key_mapping = {
        "google": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    
    variable_name = key_mapping.get(provider)
    if variable_name:
        set_key(dotenv_path, variable_name, api_key)
        print(f"✅ Successfully updated {provider.capitalize()} API key.")
    else:
        print(f"❌ Invalid provider specified: {provider}") 