#!/bin/bash
# Or #!/bin/zsh

# --- Option 1: Simple Script (`run_paste_demo.sh`) ---

# Run the Python script and capture its standard output
# Use python3 if python defaults to python2 on your system
command_output=$(python inline_paste_demo.py)

# Check if the script produced any output (i.e., didn't exit early/empty)
if [[ -n "$command_output" ]]; then
  # Use read -e to enable readline editing, -i to set initial text
  # The prompt (-p) is optional but helpful
  read -e -p "> " -i "$command_output" user_final_command
  # At this point, $user_final_command contains what the user confirmed
  # You could potentially execute it directly here if desired:
  # eval "$user_final_command"
  # Or just let the script exit, leaving the command on the prompt history
  echo "" # Add a newline for cleaner terminal output after read finishes
  echo "You finalized: $user_final_command" # Optional confirmation
else
  echo "Operation cancelled or no input provided."
fi


# --- Option 2: Shell Function (add to ~/.bashrc or ~/.zshrc) ---
# function run_paste_demo() {
#   local command_output
#   local user_final_command
#
#   command_output=$(python /path/to/inline_paste_demo.py) # Use absolute path if needed
#
#   if [[ -n "$command_output" ]]; then
#     read -e -p "> " -i "$command_output" user_final_command
#     # If you want the command to be added to history and potentially executed
#     # immediately after you press Enter on the 'read' prompt, you might need
#     # shell-specific tricks or simply rely on the user pressing Enter again
#     # on the pre-filled line. The simplest is often just letting 'read' populate
#     # the buffer. For Zsh, you can use print -z "$user_final_command"
#     # For Bash, you might need workarounds or just accept the 'read' behaviour.
#     # Let's just print it for demonstration:
#     echo ""
#     echo "You finalized: $user_final_command"
#     # To add to history (Bash/Zsh):
#     history -s -- "$user_final_command"
#   else
#     echo "Operation cancelled or no input provided."
#   fi
# }
# After adding to rc file, run: source ~/.bashrc (or ~/.zshrc)
# Then you can just type `run_paste_demo` in your terminal.