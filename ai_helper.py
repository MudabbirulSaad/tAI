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
    
    .hidden {
        display: none;
    }
    """

    BINDINGS = [
        Binding("escape", "quit", "Exit", priority=True),
        Binding("ctrl+c", "quit", "Cancel", priority=True),
    ]

    # Reactive variables
    status_text = reactive("Initializing...")
    current_command = reactive("")
    show_response = reactive(False)

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
            self.status_text = "Ready! Type your command request..."
        except Exception as e:
            self.status_text = f"Error initializing Gemini: {str(e)}"

    def watch_status_text(self, status: str) -> None:
        """Update status display when status_text changes."""
        try:
            self.query_one("#status", Static).update(status)
        except:
            # Ignore errors during initialization
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
            # Ignore errors during initialization
            pass

    @on(Input.Submitted)
    def handle_submission(self, event: Input.Submitted) -> None:
        """Called when Enter is pressed in the Input."""
        query = event.value.strip()
        if not query:
            return
        
        if not self.client:
            self.status_text = "❌ Gemini client not initialized"
            return
        
        # Clear previous response and show loading
        self.current_command = ""
        self.status_text = "🔄 Generating command..."
        
        # Start AI processing
        self.generate_command(query)

    @work(exclusive=True)
    async def generate_command(self, query: str) -> None:
        """Generate command using Gemini AI with structured output."""
        try:
            # Create a detailed prompt for Linux command generation
            prompt = """You are a Linux command expert. Generate a single, executable Linux command for the following request:

Requirements:
- Return ONLY the command, no explanations or markdown
- The command should be safe and appropriate for a Linux system
- If the request is unclear, provide the most reasonable interpretation
- Do not include sudo unless absolutely necessary
- Prefer commonly available tools (ls, find, grep, awk, etc.)"""

            class Command(BaseModel):
                command: str

            # Generate response
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
            
            command = response.text
            command_data = json.loads(command)
            command = command_data["command"]
            
            # Update the UI
            self.current_command = command
            self.status_text = "✅ Command generated! Press Enter to paste to terminal, Esc to exit"
            
            # Automatically paste to terminal
            await self.paste_to_terminal(command)
            
        except Exception as e:
            self.status_text = f"❌ Error: {str(e)}"

    async def paste_to_terminal(self, command: str) -> None:
        """Paste the generated command to the terminal."""
        try:
            # Use xdotool to paste to the terminal
            await asyncio.to_thread(
                subprocess.run,
                ["xdotool", "type", "--clearmodifiers", command],
                check=True
            )
            self.status_text = "✅ Command pasted! Continue typing or press Esc to exit"
        except subprocess.CalledProcessError:
            # Fallback: copy to clipboard
            try:
                await asyncio.to_thread(
                    subprocess.run,
                    ["xclip", "-selection", "clipboard"],
                    input=command.encode(),
                    check=True
                )
                self.status_text = "📋 Command copied to clipboard (xdotool not available)"
            except subprocess.CalledProcessError:
                # Final fallback: just show the command
                self.status_text = "⚠️ Could not paste. Command shown above - copy manually"

    def action_quit(self) -> None:
        """Exit the application."""
        self.exit()

def main():
    """Main entry point."""
    # Check for required dependencies
    try:
        from google import genai
        import dotenv
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check for API key
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please create a .env file with your Gemini API key:")
        print("GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Run the app
    app = AIHelperApp()
    app.run(inline=True)

if __name__ == "__main__":
    main() 