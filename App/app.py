import os
import sys
import subprocess
import asyncio
import time
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Input, Label, Static, Select
from textual.reactive import reactive
from textual import on, work
from textual.binding import Binding
from textual.worker import Worker

from LLM.LLM_Integration import llm
from App.models import MODEL_DICT
from typing import List

class TAI(App):

    # Cursor-like styling for the popup
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("escape", "quit", "Exit", priority=True),
        Binding("ctrl+c", "quit", "Cancel", priority=True),
        Binding("ctrl+e", "toggle_mode", "Toggle Execute/Paste Mode", priority=True),
    ]

    # Reactive variables
    status_text = reactive("Initializing...")
    current_command = reactive("")
    command_output = reactive("")
    show_response = reactive(False)
    show_output = reactive(False)
    execute_mode = reactive(False)  # False = paste mode (default), True = execute mode
    pending_paste_command = None  # Store command to paste after exit

    def __init__(self):
        super().__init__()
        self.model_dict = MODEL_DICT
        self.default_model_value = "openrouter/mistralai/devstral-small:free"
        self.model = self.default_model_value

        # Find the key for the default model value to set as the initial Select value
        self.default_model_key = [k for k, v in self.model_dict.items() if v == self.default_model_value][0]

    def compose(self) -> ComposeResult:
        """Create child widgets for the popup."""
        yield Container(
            Static("🤖 AI Command Helper", id="title"),
            Select(
                options=[(name, name) for name in self.model_dict.keys()],
                value=self.default_model_key,
            ),
            Input(
                placeholder="e.g., 'list all files larger than 100MB'",
                id="input"
            ),
            Static(self.status_text, id="status"),
            Static("", id="response", classes="hidden"),
            Static("", id="output", classes="hidden"),
            id="main_container"
        )

    def on_mount(self) -> None:
        """Focus input on start and setup LLM."""
        self.query_one("#input", Input).focus()
        self.setup_llm()

    def setup_llm(self):
        """Initialize LLM"""
        try:
            self.llm = llm()
            mode = "EXECUTE" if self.execute_mode else "PASTE"
            self.status_text = f"Ready! Mode: {mode} (Ctrl+E to toggle) | Type your command request..."
        except Exception as e:
            self.status_text = f"Error initializing LLM: {str(e)}"

    def watch_status_text(self, status: str) -> None:
        """Update status display when status_text changes."""
        try:
            self.query_one("#status", Static).update(status)
        except:
            pass

    def watch_current_command(self, command: str) -> None:
        """Update response display when current_command changes."""
        try:
            response_widget = self.query_one("#response", Static)
            if command:
                response_widget.update(f"Generated: {command}")
                response_widget.remove_class("hidden")
                self.show_response = True
            else:
                response_widget.add_class("hidden")
                self.show_response = False
        except:
            pass

    def watch_command_output(self, output: str) -> None:
        """Update output display when command_output changes."""
        try:
            output_widget = self.query_one("#output", Static)
            if output:
                output_widget.update(f"Output:\n{output}")
                output_widget.remove_class("hidden")
                self.show_output = True
            else:
                output_widget.add_class("hidden")
                self.show_output = False
        except:
            pass

    def watch_execute_mode(self, mode: bool) -> None:
        """Update status when mode changes."""
        if self.llm:  # Only update if initialized
            mode_text = "EXECUTE" if mode else "PASTE"
            self.status_text = f"Ready! Mode: {mode_text} (Ctrl+E to toggle) | Type your command request..."

    def action_toggle_mode(self) -> None:
        """Toggle between execute and paste modes."""
        self.execute_mode = not self.execute_mode
        # Clear previous outputs when switching modes
        self.command_output = ""

    @on(Select.Changed)
    def handle_llm_change(self, event: Select.Changed) -> None:
        """Called when the LLM is changed."""
        self.model = self.model_dict[str(event.value)]

    @on(Input.Submitted)
    def handle_submission(self, event: Input.Submitted) -> None:
        """Called when Enter is pressed in the Input."""
        query = event.value.strip()
        if not query:
            return
        
        if not self.llm:
            self.status_text = "❌ LLM not initialized"
            return
        
        # Clear previous responses
        self.current_command = ""
        self.command_output = ""
        self.status_text = "🔄 Generating command..."
        
        # Start AI processing
        self.generate_command(self.model,query)

    @work(exclusive=True)
    async def generate_command(self, model: str, query: str) -> None:
        """Generate command using Gemini AI with structured output."""
        try:
            
            # Generate response using Edward's suggestion: extract JSON properly
            command = await asyncio.to_thread(
                self.llm.generate_command,
                model,
                query
            )
            
            if self.execute_mode:
                self.status_text = "✅ Command generated! Executing..."
                # Execute the command directly (Edward's suggestion)
                await self.execute_command(command)
            else:
                self.status_text = "✅ Command generated! Exiting and pasting to terminal..."
                # Store command and exit to paste (your shell_script approach)
                self.pending_paste_command = command
                # Small delay to show the message
                await asyncio.sleep(1)
                self.exit(result=command)  # Exit with the command to paste
            
        except Exception as e:
            self.status_text = f"❌ Error: {str(e)}"

    @work(thread=True)  # Using Edward's threaded worker approach
    def execute_command(self, command: str) -> None:
        """Execute command directly using subprocess (Edward's approach)."""
        try:
            # Run the command as Edward suggested
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # Prevent hanging
            )
            
            # Combine stdout and stderr
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            
            if not output.strip():
                output = f"Command executed successfully (exit code: {result.returncode})"
            
            # Update UI from worker thread
            self.call_from_thread(self._update_after_execution, output, result.returncode)
            
        except subprocess.TimeoutExpired:
            self.call_from_thread(self._update_after_execution, "Command timed out after 30 seconds", 1)
        except Exception as e:
            self.call_from_thread(self._update_after_execution, f"Error executing command: {str(e)}", 1)

    def _update_after_execution(self, output: str, exit_code: int) -> None:
        """Update UI after command execution."""
        self.command_output = output
        if exit_code == 0:
            self.status_text = "✅ Command executed successfully! Press Esc to exit or continue..."
        else:
            self.status_text = f"⚠️ Command failed (exit code: {exit_code}). Press Esc to exit or continue..."

    def action_quit(self) -> None:
        """Exit the application."""
        self.exit()