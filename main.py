import argparse
from App.app import TAI
from KeyAutomation import Automate
from Utils.api_key_manager import update_api_key
from Utils.config_manager import set_default_model
from App.models import MODEL_DICT

def main():
    parser = argparse.ArgumentParser(description="🤖 AI Command Helper", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--google", type=str, help="Set the Google Gemini API key")
    parser.add_argument("--openai", type=str, help="Set the OpenAI API key")
    parser.add_argument("--anthropic", type=str, help="Set the Anthropic API key")
    parser.add_argument("--openrouter", type=str, help="Set the OpenRouter API key")
    parser.add_argument("--default-model", type=str, help="Set the default model for the application")
    parser.add_argument("--models", action="store_true", help="List all available models")
    args = parser.parse_args()

    if args.models:
        print("Available models:")
        for name, identifier in MODEL_DICT.items():
            print(f"- {name}: {identifier}")
        return

    if args.default_model:
        if args.default_model in MODEL_DICT.values():
            set_default_model(args.default_model)
            print(f"✅ Default model set to: {args.default_model}")
        else:
            print(f"❌ Error: Model '{args.default_model}' not found.")
            print("Please use the --models flag to see the list of available models.")
        return
        
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