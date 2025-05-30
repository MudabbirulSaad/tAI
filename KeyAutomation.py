import time
import subprocess

class Automate():
    def __init__(self):
        self.command = None

    def paste_command_to_terminal(self, command: str) -> None:
        """Paste command to terminal using xdotool after TUI exits."""
        try:
            # print(f"Pasting command: {command}")
            time.sleep(0.5)
            subprocess.run([
                "xdotool", "type", "--clearmodifiers", command
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pasting command: {e}")
            print(f"💡 Manual copy: {command}")
        except FileNotFoundError:
            print("❌ xdotool not found. Please install: sudo apt install xdotool")
            print(f"💡 Manual copy: {command}")