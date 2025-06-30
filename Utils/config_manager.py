"""
This module handles reading and writing configuration from config.json.
"""
import json
import os

CONFIG_FILE = "config.json"

def get_config() -> dict:
    """Reads the configuration from config.json."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def get_default_model() -> str:
    """Gets the default model from the configuration."""
    config = get_config()
    return config.get("default_model", "openrouter/mistralai/devstral-small:free")

def set_default_model(model_id: str) -> None:
    """Sets the default model in the configuration."""
    config = get_config()
    config["default_model"] = model_id
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2) 