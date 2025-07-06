# tAI (terminal-AI) 🤖

**tAI** is a minimal integration of AI inside CLI. No it's neither a `chatting application` and nor a clone of `claude code` or `gemini cli`. **The goal is to have a minimal AI assistant for quick reference of terminal commands.** The project was inspired from the **cursor** AI popup inside the terminal. I wanted to build something similar but outside of cursor where based on natural language it'll generate the command and paste it inside the terminal. No need for fance `wrap` or other CLI tools. This tool will only generate command based on the natural language and paste it inside the terminal without sharing anything from the terminal.

## Special Thanks
- **[Textual](https://textual.textualize.io/):** For the amazing TUI framework.
- **[Litellm](https://www.litellm.ai/):** For the amazing API wrapper for multiple LLMs.

## Features

- 🎯 **Inline TUI Popup**: Small popup overlay that doesn't take over the entire terminal
- 🖥️ **Fullscreen Mode**: A fullscreen mode for those who want to use it in full screen
- 🤖 **Powered by 21 LLMs**: Use upto **21 LLMs** including `gemini flash 2.5` and others
- 🤗 **Free usage**: **8 free models** available to test it out without giving any **API** keys
- ⚡ **Auto-Paste**: Automatically pastes generated commands to your terminal
- 🪓 **Auto-execution**: Automatically execute the generated commands (use it with **caution**)
- 🎨 **Minimal Styling**: Minimalistic design
- ⌨️ **Simple Controls**: ESC to exit, Enter to generate commands
- 🔧 **Settings from TUI**: A settings page to change all settings (api key, default model, etc)
- 📝 **Custom Prompt Config:** Customize prompt for personal usage.
- 🔐 **Security**: Do not share anything from the terminal while calling the API.

## Demo

### Inline Mode

![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/CxFXZ84qlzgUma9G6yErO.png)

### Fullscreen mode
![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/FoJOmIhm0BBaw0ro46c9q.png)

### Video demo

![](https://private-user-images.githubusercontent.com/59968346/462934040-1d6e32ec-2a0b-4933-9788-cd94a4ac7628.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTE4MTU3NTAsIm5iZiI6MTc1MTgxNTQ1MCwicGF0aCI6Ii81OTk2ODM0Ni80NjI5MzQwNDAtMWQ2ZTMyZWMtMmEwYi00OTMzLTk3ODgtY2Q5NGE0YWM3NjI4Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA3MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNzA2VDE1MjQxMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTgyNDY3MDA3NTcyMDlkOGYzZjEyODhhMGUzNDczYjdhMzliMGNjZGI5MDgxMjdjMDQwMzQ3YTQyOGFmMDMyNmQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.AAo2GTUA_Ppr_0FnhAVbTHL58JvhkSsyua39wiYIyaY)

## Installation

### Prerequisites

- **Python 3.12** or higher
- **Linux Debian** based distribution (i.e: `Ubuntu`)

### Instal Directly

1. **Download the `tai_1.0.0.deb` file** from the [**releases**](https://github.com/KillerShoaib/tAI/releases/download/v0.0.1/tai_0.0.1.deb)

2. **Install `.deb` file**:

   ```bash
   sudo apt install ./tai_1.0.0.deb
   ```


### Installation from source

1. **Clone the repository**

   ```bash
   git clone https://github.com/KillerShoaib/tAI.git
   ```

2. **Go to project directory**:
   ```bash
   cd tAI
   ```

3. **Run the `install.bash`**:
   ```bash
   bash install.bash
   ```

That's it! It'll build the `.deb` file and install the file. It may ask for password before installtion.

## Usage

### Basic Usage

Simply run the application using this command
```bash
tai
```

### Command Line Arguments

| Argument            | Type    | Description                                                                                         | Example Usage                                 |
|---------------------|---------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------|
| `--google`          | string  | Set the Google Gemini API key                                                                       | `--google YOUR_GOOGLE_API_KEY`                |
| `--openai`          | string  | Set the OpenAI API key                                                                              | `--openai YOUR_OPENAI_API_KEY`                |
| `--anthropic`       | string  | Set the Anthropic API key                                                                           | `--anthropic YOUR_ANTHROPIC_API_KEY`          |
| `--openrouter`      | string  | Set the OpenRouter API key                                                                          | `--openrouter YOUR_OPENROUTER_API_KEY`        |
| `--default-model`   | string  | Set the default model for the application (must match an available model identifier)                | `--default-model openai/gpt-4o`               |
| `--models`          | flag    | List all available models and their identifiers                                                     | `--models`                                    |
| `--fullscreen`      | string  | Set fullscreen mode (`true` or `false`)                                                             | `--fullscreen true` or `--fullscreen false`   |

**Notes:**
- You can combine arguments as needed. For example, to set an API key and the default model in one command.
- Use `tai --models` to see all available model names and identifiers.

### Settings from TUI

#### Default Model

Change the default model for the application itself.

![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/TWMb8O5VtXTlJozmpQK3m.png)



#### Setup API Keys

Set the API keys for the models you want to use. Currently supports 4 provider APIs:

- **Google (Gemini)**
- **OpenAI (GPT)**
- **Anthropic (Claude)**
- **OpenRouter (All models)**

![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/ggxXlEefGquXaVubzvXLD.png)

#### Custom Prompt

Customize the prompt for your personal usage.

![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/DXGusMbv208fLe33MGtc1.png)

#### Other Settings

- **Fullscreen Mode**: Set the fullscreen mode from the `Others` section.

- **Openrouter For All models**: Set the openrouter for all models. So you can pass only the openrouter API key and it'll be used for all models. **But free openrouter API key then won't work (even for the free model).**

![](https://cdn-uploads.huggingface.co/production/uploads/65ca6f0098a46a56261ac3ac/ecXKLHI00X9VhpNoipiHx.png)

> **Note:** If `Set openrouter for all models` is `true`, then the free `OpenRouter` API key won't work (even for the free model).

## Free OpenRouter API Key

- **Access to free models**: You have access to free models from `OpenRouter` API via free openrouter API key which I've exposed so that you can get a test out the application (don't worry, it's a free API key so I won't be getting broked).
- **Limited Usage**: Since this is a free API key therefore it's usage is going to be very very limited because of the rate limits and single API key for every user (variable based on the model) and the performance is going to be very slow.

## Free API Keys (alternative)

- **Google (Gemini)**: If you want more usage, you can get a free API key from [*Google AI Studio*](https://aistudio.google.com/). Just copy the API key and paste it in the `API Keys` section.


## Controls

- **Enter**: Generate command from your query
- **ESC**: Exit the popup or fullscreen mode
- **Ctrl+c**: Exit the popup or fullscreen mode
- **Ctrl+e**: Toggle between paste and execute mode.

## Keybindings in terminal

If you want to replicate the similar behavior of `cursor` where you can press `Ctrl+k` to open the AI popup, you can do that by adding the following to your `.bashrc` file:

```bash
# === tAI Keybinding ===
ai_helper() {
    tai

    printf "\r\033[K"
}

# Bind Ctrl+K to launch the ai_helper function.
bind -x '"\C-k": ai_helper'
```

Add the above code to your `.bashrc` file and then run `source ~/.bashrc` to apply the changes.


## TODO List

- [x] Multi model support
- [x] Settings from TUI
- [x] Custom prompt configuration
- [x] Fullscreen mode
- [x] Command line arguments
- [x] Bash integration with keybinding
- [x] Free openrouter API key
- [x] Deb package installation
- [x] CICD pipeline
- [ ] Integration of Context (current path, previous commands, previous response)
- [ ] Support for Windows, MacOS and other Linux distributions
- [ ] PyPI package installation
- [ ] Docker image (or container)
- [ ] apt repository

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed. 