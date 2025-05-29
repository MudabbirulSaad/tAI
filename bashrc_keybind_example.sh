# AI Helper Keybinding for .bashrc
# Add these lines to your ~/.bashrc file

# Function to launch AI Helper
ai_helper() {
    # Get the current directory to return to it after
    local current_dir=$(pwd)
    
    # Launch the AI helper
    python3 ~/Personal/Personal\ projects/CmdAI/ai_helper.py
    
    # Optional: Clear the line after the helper exits (clean up any artifacts)
    printf "\r\033[K"
}

# Create the keybinding - Ctrl+K (like Cursor)
bind -x '"\C-k": ai_helper'

# Alternative keybindings you could use instead:
# bind -x '"\C-j": ai_helper'           # Ctrl+J
# bind -x '"\ea": ai_helper'            # Alt+A  
# bind -x '"\e\C-h": ai_helper'         # Alt+Ctrl+H
# bind -x '"\C-x\C-a": ai_helper'       # Ctrl+X, Ctrl+A (two key sequence)

# Optional: Add an alias for manual launching
alias aih='python3 ~/Personal/Personal\ projects/CmdAI/ai_helper.py'

echo "🤖 AI Helper loaded! Press Ctrl+K to activate" 