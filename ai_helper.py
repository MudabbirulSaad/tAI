#!/usr/bin/env python3
"""
AI Command Helper - A TUI popup for generating Linux commands using Gemini AI
"""

import os
import sys
import subprocess
import asyncio
from typing import Optional
from pydantic import BaseModel

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Input, Label, Static
from textual.reactive import reactive
from textual import on, work
from textual.binding import Binding
from textual.worker import Worker

from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class CommandResponse(BaseModel):
    """Structured output for command generation"""
    command: str
    explanation: Optional[str] = None

class AIHelperApp(App):
    """A Textual app that generates Linux commands using AI and pastes them to terminal."""

    # Cursor-like styling for the popup
    CSS = """
    Screen {
        background: transparent;
    }
    
    Container {
        background: $surface;
        border: thick $primary;
        width: 80%;
        height: auto;
        margin: 1 2;
        padding: 1;
    }
    
    #title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #input {
        border: solid $accent;
        background: $surface-lighten-1;
        margin: 1 0;
    }
    
    #status {
        color: $text-muted;
        text-align: center;
        margin-top: 1;
        height: 1;
    }
    
    #response {
        background: $surface-darken-1;
        border: solid $success;
        padding: 1;
        margin-top: 1;
        color: $success;
        text-style: bold;
        min-height: 3;
    }
    
    #output {
        background: $surface-darken-2;
        border: solid $warning;
        padding: 1;
        margin-top: 1;
        color: $warning;
        min-height: 3;
        max-height: 10;
        overflow-y: auto;
    }
    
    .hidden {
        display: none;
    }
    """

    BINDINGS = [
        Binding("escape", "quit", "Exit", priority=True),
        Binding("ctrl+c", "quit", "Cancel", priority=True),
        Binding("ctrl+e", "toggle_mode", "Toggle Execute/Copy Mode", priority=True),
    ]

    # Reactive variables
    status_text = reactive("Initializing...")
    current_command = reactive("")
    command_output = reactive("")
    show_response = reactive(False)
    show_output = reactive(False)
    execute_mode = reactive(True)  # True = execute, False = copy to clipboard

    def __init__(self):
        super().__init__()
        self.client = None
        self.model = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the popup."""
        yield Container(
            Static("🤖 AI Command Helper", id="title"),
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
        """Focus input on start and setup Gemini."""
        self.query_one("#input", Input).focus()
        self.setup_gemini()

    def setup_gemini(self):
        """Initialize Gemini AI client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.status_text = "Error: GEMINI_API_KEY not found in environment"
            return
        
        try:
            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.0-flash"
            mode = "EXECUTE" if self.execute_mode else "COPY"
            self.status_text = f"Ready! Mode: {mode} (Ctrl+E to toggle) | Type your command request..."
        except Exception as e:
            self.status_text = f"Error initializing Gemini: {str(e)}"

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
        if self.client:  # Only update if initialized
            mode_text = "EXECUTE" if mode else "COPY"
            self.status_text = f"Ready! Mode: {mode_text} (Ctrl+E to toggle) | Type your command request..."

    def action_toggle_mode(self) -> None:
        """Toggle between execute and copy modes."""
        self.execute_mode = not self.execute_mode
        # Clear previous outputs when switching modes
        self.command_output = ""

    @on(Input.Submitted)
    def handle_submission(self, event: Input.Submitted) -> None:
        """Called when Enter is pressed in the Input."""
        query = event.value.strip()
        if not query:
            return
        
        if not self.client:
            self.status_text = "❌ Gemini client not initialized"
            return
        
        # Clear previous responses
        self.current_command = ""
        self.command_output = ""
        self.status_text = "🔄 Generating command..."
        
        # Start AI processing
        self.generate_command(query)

    @work(exclusive=True)
    async def generate_command(self, query: str) -> None:
        """Generate command using Gemini AI with structured output."""
        try:
            prompt = """You are a Linux command expert. Generate a single, executable Linux command for the following request:

Requirements:
- Return ONLY the command, no explanations or markdown
- The command should be safe and appropriate for a Linux system
- If the request is unclear, provide the most reasonable interpretation
- Do not include sudo unless absolutely necessary
- Prefer commonly available tools (ls, find, grep, awk, etc.)"""

            class Command(BaseModel):
                command: str

            # Generate response using Edward's suggestion: extract JSON properly
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=prompt,
                    response_mime_type="application/json",
                    response_schema=Command,    
                ),
                contents=query,
            )
            
            # Extract JSON response and convert to Python variables (Edward's approach)
            command_json = response.text
            command_data = json.loads(command_json)  # Using json.loads as Edward suggested
            command = command_data["command"]
            
            # Update the UI
            self.current_command = command
            
            if self.execute_mode:
                self.status_text = "✅ Command generated! Executing..."
                # Execute the command directly (Edward's suggestion)
                await self.execute_command(command)
            else:
                self.status_text = "✅ Command generated and copied to clipboard!"
                # Copy to clipboard
                await self.copy_to_clipboard(command)
            
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
                # capture_output=True,
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

    async def copy_to_clipboard(self, command: str) -> None:
        """Copy command to clipboard."""
        try:
            await asyncio.to_thread(
                subprocess.run,
                ["xclip", "-selection", "clipboard"],
                input=command.encode(),
                check=True
            )
            self.status_text = "📋 Command copied to clipboard! Press Ctrl+Shift+V in terminal to paste"
        except subprocess.CalledProcessError:
            self.status_text = "⚠️ Could not copy to clipboard. Command shown above - copy manually"

    def action_quit(self) -> None:
        """Exit the application."""
        self.exit()

def main():
    """Main entry point."""
    try:
        from google import genai
        import dotenv
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please create a .env file with your Gemini API key:")
        print("GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    app = AIHelperApp()
    app.run(inline=True)

if __name__ == "__main__":
    main() 