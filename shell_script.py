import subprocess
import time

command_to_type = "cd .."

print("You have 5 seconds to focus the terminal window...")
time.sleep(5) # Time to focus the terminal

# This assumes xdotool is installed and you're in an X11 session
try:
    # Get the active window ID (hopefully your terminal)
    # This part can be tricky to make robust
    # active_window_id = subprocess.check_output("xdotool getactivewindow", shell=True).decode().strip()
    # subprocess.run(f"xdotool type --window {active_window_id} '{command_to_type}'", shell=True, check=True)
    # subprocess.run(f"xdotool key --window {active_window_id} Return", shell=True, check=True)

    # Simpler: just type to the currently focused window
    subprocess.run(f"xdotool type '{command_to_type}'", shell=True, check=True)
    # subprocess.run(f"xdotool key Return", shell=True, check=True)
    print("Command typed using xdotool.")
except Exception as e:
    print(f"Error using xdotool: {e}")
    print("Make sure xdotool is installed and you are in a graphical environment.")