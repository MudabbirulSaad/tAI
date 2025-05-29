# AI Command Helper 🤖

A terminal UI (TUI) popup that generates Linux commands using Google's Gemini AI, similar to Cursor's integrated terminal popup.

## Features

- 🎯 **Inline TUI Popup**: Small popup overlay that doesn't take over the entire terminal
- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash for intelligent command generation
- ⚡ **Auto-Paste**: Automatically pastes generated commands to your terminal
- 🎨 **Cursor-like Styling**: Modern, clean interface inspired by Cursor's design
- ⌨️ **Simple Controls**: ESC to exit, Enter to generate commands
- 🔄 **Continuous Use**: Keep the popup open for multiple queries

## Prerequisites

- Python 3.8+
- Linux system with X11 (for terminal pasting)
- Google Gemini API key

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies** (for terminal pasting):
   ```bash
   # Ubuntu/Debian
   sudo apt install xdotool xclip

   # Fedora/RHEL
   sudo dnf install xdotool xclip

   # Arch Linux
   sudo pacman -S xdotool xclip
   ```

4. **Set up your API key**:
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project directory:
     ```bash
     echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
     ```

## Usage

### Basic Usage

Run the AI helper:
```bash
python ai_helper.py
```

### How it works

1. **Launch**: Run the script to open the popup
2. **Type**: Enter your command request in natural language
   - Example: "list all files larger than 100MB"
   - Example: "find Python files modified in the last week"
   - Example: "show disk usage sorted by size"
3. **Generate**: Press Enter to generate the command
4. **Auto-paste**: The command is automatically pasted to your terminal
5. **Continue or Exit**: 
   - Type another query for a new command
   - Press ESC to close the popup

### Example Queries

- `"list all files larger than 100MB"`
- `"find Python files modified in the last week"`
- `"show disk usage sorted by size"`
- `"kill all processes containing 'python'"`
- `"compress all .log files in current directory"`
- `"show network connections on port 8080"`

## Controls

- **Enter**: Generate command from your query
- **ESC**: Exit the popup
- **Ctrl+C**: Exit the popup

## Features Explained

### Inline Mode
The app uses Textual's `inline=True` mode to create a small popup overlay instead of taking over the entire terminal.

### AI Integration
- Uses Google's Gemini 2.0 Flash model for fast, accurate command generation
- Structured prompting ensures Linux-appropriate commands
- Automatic cleanup of AI response formatting

### Terminal Pasting
- Primary method: Uses `xdotool` to type directly into the terminal
- Fallback 1: Copies to clipboard using `xclip`
- Fallback 2: Displays command for manual copying

### Styling
- Cursor-inspired design with modern borders and colors
- Responsive layout that adapts to terminal size
- Clear status indicators and visual feedback

## Troubleshooting

### "xdotool not found"
Install xdotool: `sudo apt install xdotool` (Ubuntu/Debian)

### "API key not found"
Make sure your `.env` file exists and contains: `GEMINI_API_KEY=your_key`

### "Command not pasted"
- Ensure xdotool is installed
- Check that your terminal supports X11
- The command will be copied to clipboard as fallback

### "Import errors"
Run: `pip install -r requirements.txt`

## Future Enhancements

- [ ] Add bash integration with keybinding (e.g., Ctrl+K)
- [ ] Support for multi-line commands
- [ ] Command history and favorites
- [ ] Different AI models support
- [ ] Wayland support for pasting

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed. 