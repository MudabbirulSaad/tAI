import argparse
from App.app import TAI
from KeyAutomation import Automate
from Utils.api_key_manager import update_api_key

def main():
    parser = argparse.ArgumentParser(description="🤖 AI Command Helper")
    parser.add_argument("--google", type=str, help="Set the Google Gemini API key")
    parser.add_argument("--openai", type=str, help="Set the OpenAI API key")
    parser.add_argument("--anthropic", type=str, help="Set the Anthropic API key")
    parser.add_argument("--openrouter", type=str, help="Set the OpenRouter API key")
    args = parser.parse_args()

    api_keys_to_update = {
        "google": args.google,
        "openai": args.openai,
        "anthropic": args.anthropic,
        "openrouter": args.openrouter,
    }

    updated = False
    for provider, key in api_keys_to_update.items():
        if key:
            update_api_key(provider, key)
            updated = True

    if updated:
        return

    automate = Automate()
    app = TAI()
    result = app.run(inline=True)
    if result is not None:
        automate.paste_command_to_terminal(result)

if __name__ == "__main__":
    main()