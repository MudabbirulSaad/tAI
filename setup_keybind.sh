#!/bin/bash
# Setup script to add AI Helper keybinding to .bashrc

echo "🚀 Setting up AI Helper keybinding..."

# Get the current directory (where ai_helper.py is located)
CURRENT_DIR=$(pwd)
AI_HELPER_PATH="$CURRENT_DIR/ai_helper.py"

# Check if ai_helper.py exists
if [ ! -f "$AI_HELPER_PATH" ]; then
    echo "❌ Error: ai_helper.py not found in current directory"
    echo "Please run this script from the directory containing ai_helper.py"
    exit 1
fi

# Create the keybinding code
KEYBIND_CODE="
# === AI Helper Keybinding ===
# Added by AI Helper setup script
ai_helper() {
    python3 \"$AI_HELPER_PATH\"
    printf \"\r\033[K\"  # Clear line after exit
}

# Bind Ctrl+K to launch AI Helper (like Cursor)
bind -x '\"\C-k\": ai_helper'

# Alternative: uncomment one of these if Ctrl+K conflicts:
# bind -x '\"\C-j\": ai_helper'           # Ctrl+J
# bind -x '\"\ea\": ai_helper'            # Alt+A

# Alias for manual launching
alias aih='python3 \"$AI_HELPER_PATH\"'
# === End AI Helper ===
"

# Backup .bashrc
echo "📋 Creating backup of .bashrc..."
cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)

# Check if AI Helper section already exists
if grep -q "AI Helper Keybinding" ~/.bashrc; then
    echo "⚠️  AI Helper keybinding already exists in .bashrc"
    echo "Do you want to replace it? (y/N)"
    read -r response
    if [[ $response =~ ^[Yy]$ ]]; then
        # Remove old section
        sed -i '/# === AI Helper Keybinding ===/,/# === End AI Helper ===/d' ~/.bashrc
        echo "$KEYBIND_CODE" >> ~/.bashrc
        echo "✅ Updated AI Helper keybinding in .bashrc"
    else
        echo "❌ Cancelled"
        exit 0
    fi
else
    # Add new section
    echo "$KEYBIND_CODE" >> ~/.bashrc
    echo "✅ Added AI Helper keybinding to .bashrc"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the keybinding:"
echo "1. Reload your .bashrc: source ~/.bashrc"
echo "2. Or open a new terminal"
echo ""
echo "Usage:"
echo "• Press Ctrl+K to launch AI Helper"
echo "• Type 'aih' to launch manually"
echo ""
echo "The AI Helper will:"
echo "• Generate commands in PASTE mode (default)"
echo "• Exit and paste the command to your terminal"
echo "• Press Ctrl+E in the helper to toggle EXECUTE mode" 