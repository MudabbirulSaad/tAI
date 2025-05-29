#!/usr/bin/env python
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Input, Label
from textual import on

class InlinePasteApp(App):
    """A Textual app that takes input and prepares it for shell pasting."""

    # Minimal CSS - adjust if needed
    CSS = """
    Screen {
        # height: auto; /* Let container determine height */
        # min_height: 3; /* Ensure at least input and label show */
        # overflow: hidden; /* Avoid scrollbars in simple inline case */
    }
    Container {
        height: auto;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit_with_error", "Cancel"), # Exit without output
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Container(
            Label("Enter command/text below, press Enter to finish:"),
            Input(placeholder="Type here...", id="main_input")
        )

    def on_mount(self) -> None:
        """Focus input on start."""
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def handle_submission(self, event: Input.Submitted) -> None:
        """Called when Enter is pressed in the Input."""
        # Exit the app, passing the input value as the result
        self.exit(result=event.value)

    def action_quit_with_error(self) -> None:
        """Exit without providing a result, potentially signalling cancellation."""
        # Exiting with None or using a different exit code could be used
        # by the wrapper script to detect cancellation. For simplicity,
        # we'll exit normally, but the wrapper won't get output to paste.
        self.exit() # Exit without a result

# --- Main execution block ---
if __name__ == "__main__":
    app = InlinePasteApp()
    # Run inline, capture the result passed to self.exit()
    result = app.run(inline=True)
    # result = app.run()
    # If the app exited with a result (i.e., Enter was pressed),
    # print that result to standard output. The shell wrapper will capture this.
    if result is not None:
        print(result, end='') # Print without trailing newline is often better for pasting
        # Note: stderr is still available for debug messages if needed during run()

    # If result is None (e.g., Ctrl+C was pressed), nothing is printed.