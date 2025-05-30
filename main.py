from App.app import TAI
from KeyAutomation import Automate

def main():
    automate = Automate()
    app = TAI()
    result = app.run(inline=True)
    if result is not None:
        automate.paste_command_to_terminal(result)

if __name__ == "__main__":
    main()