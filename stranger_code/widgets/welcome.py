"""Welcome banner widget for Stranger Code - Enter the Upside Down."""

from __future__ import annotations

import random
from typing import Any

from textual.widgets import Static

from stranger_code._version import __version__
from stranger_code.config import STRANGER_CODE_ASCII

# Stranger Things themed welcome messages
WELCOME_MESSAGES = [
    "Ready to enter the Upside Down? What would you like to build?",
    "Friends don't lie. What code shall we write together?",
    "The Gate is open. What mysteries await?",
    "Eleven is ready. What powers shall we unleash?",
    "Hawkins Lab is online. Begin your experiment.",
]


class WelcomeBanner(Static):
    """Welcome banner displayed at startup - Enter the Upside Down."""

    DEFAULT_CSS = """
    /* ========================================
       WELCOME BANNER - The Gate Opens
       Stranger Things title treatment
       ======================================== */
    WelcomeBanner {
        height: auto;
        padding: 1;
        margin-bottom: 1;
        background: #0a0a0a;
    }
    """

    # Christmas lights colors for the "powered by deepagents" text
    LIGHT_COLORS = ["#ff0000", "#00ff00", "#0066ff", "#ffff00", "#ff6600", "#9932cc"]

    def _christmas_text(self, text: str) -> str:
        """Apply Christmas lights colors to each character."""
        result = ""
        color_idx = 0
        for char in text:
            if char == " ":
                result += " "
            else:
                color = self.LIGHT_COLORS[color_idx % len(self.LIGHT_COLORS)]
                result += f"[bold {color}]{char}[/bold {color}]"
                color_idx += 1
        return result

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the welcome banner."""
        # The ASCII art already has color formatting from config.py
        banner_text = STRANGER_CODE_ASCII
        banner_text += f"\n[dim #4a4a4a]v{__version__}[/dim #4a4a4a]"

        # Christmas lights style for "Powered by deepagents"
        powered_by = self._christmas_text("Powered by deepagents")
        banner_text += f"  {powered_by}\n"

        # Random themed welcome message
        welcome_msg = random.choice(WELCOME_MESSAGES)
        banner_text += f"[#e21b1b]{welcome_msg}[/#e21b1b]\n"

        # Themed keyboard hints
        banner_text += "[dim #6b3a3a]Enter send • Ctrl+J newline • @ files • / commands[/dim #6b3a3a]"

        super().__init__(banner_text, **kwargs)
