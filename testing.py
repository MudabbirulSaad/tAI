import time
from pynput.keyboard import Controller, Key

# The command you want to type
command = "Hello World"

# Create a keyboard controller
keyboard = Controller()

# Give yourself a few seconds to switch to the terminal window
print("Switch to your terminal window in 3 seconds...")
time.sleep(3)

# Type the command
for char in command:
    keyboard.press(char)
    keyboard.release(char)
    # Add a small delay between key presses for realism (optional)
    time.sleep(0.04)