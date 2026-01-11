"""Loading widget with Christmas lights spinner for Stranger Code."""

from __future__ import annotations

import random
from time import time
from typing import TYPE_CHECKING, ClassVar

from textual.containers import Horizontal
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.app import ComposeResult

# Portal particle characters
PARTICLES = ["·", "˚", "*", "∙", "°"]
PARTICLE_COLORS = ["#3a2020", "#4a2a2a", "#2a2a3a", "#3a3a2a"]

# Stranger Things themed loading messages
STRANGER_LOADING_MESSAGES = [
    "Entering the Upside Down",
    "Contacting Hawkins Lab",
    "Channeling Eleven's powers",
    "Opening the Gate",
    "Detecting Demogorgon activity",
    "Decoding Vecna's signal",
    "Searching the Void",
    "Activating sensory deprivation tank",
    "Tuning into the Mind Flayer",
    "Investigating Starcourt Mall",
    "Checking the Russian base",
]


class ChristmasLightsSpinner:
    """Animated Christmas lights spinner - like Joyce's wall.

    Cycles through colors: red, green, blue, yellow, orange
    Just like the lights Joyce used to communicate with Will!
    """

    # Christmas lights colors
    COLORS: ClassVar[tuple[str, ...]] = (
        "#ff0000",  # Red
        "#00ff00",  # Green
        "#0066ff",  # Blue
        "#ffff00",  # Yellow
        "#ff6600",  # Orange
    )

    # Light bulb characters for variety
    BULBS: ClassVar[tuple[str, ...]] = (
        "●",
        "◉",
        "○",
        "◎",
        "◐",
    )

    def __init__(self) -> None:
        """Initialize spinner."""
        self._position = 0
        self._bulb_index = 0

    def next_frame(self) -> str:
        """Get next animation frame with color."""
        color = self.COLORS[self._position]
        bulb = self.BULBS[self._bulb_index]
        self._position = (self._position + 1) % len(self.COLORS)
        # Change bulb style occasionally
        if self._position == 0:
            self._bulb_index = (self._bulb_index + 1) % len(self.BULBS)
        return f"[{color}]{bulb}[/{color}]"

    def current_frame(self) -> str:
        """Get current frame without advancing."""
        color = self.COLORS[self._position]
        bulb = self.BULBS[self._bulb_index]
        return f"[{color}]{bulb}[/{color}]"


class LoadingWidget(Static):
    """Animated loading indicator with Christmas lights and Stranger Things messages.

    Displays: ● Entering the Upside Down... (3s, esc to interrupt)
    """

    DEFAULT_CSS = """
    /* ========================================
       LOADING WIDGET - Christmas Lights
       Joyce's wall communication style
       ======================================== */
    LoadingWidget {
        height: auto;
        padding: 0 1;
        background: #0a0a0a;
    }

    LoadingWidget .loading-container {
        height: auto;
        width: 100%;
    }

    LoadingWidget .loading-spinner {
        width: auto;
    }

    LoadingWidget .loading-status {
        width: auto;
        color: #e21b1b;
        text-style: italic;
    }

    LoadingWidget .loading-hint {
        width: auto;
        color: #6b3a3a;
        margin-left: 1;
    }

    LoadingWidget .loading-particles {
        width: auto;
        margin-left: 1;
    }
    """

    def __init__(self, status: str | None = None) -> None:
        """Initialize loading widget.

        Args:
            status: Initial status text to display (uses random Stranger message if None)
        """
        super().__init__()
        self._status = status or random.choice(STRANGER_LOADING_MESSAGES)
        self._spinner = ChristmasLightsSpinner()
        self._start_time: float | None = None
        self._spinner_widget: Static | None = None
        self._status_widget: Static | None = None
        self._hint_widget: Static | None = None
        self._particles_widget: Static | None = None
        self._paused = False
        self._paused_elapsed: int = 0
        self._message_change_counter = 0

    def compose(self) -> ComposeResult:
        """Compose the loading widget layout."""
        with Horizontal(classes="loading-container"):
            self._spinner_widget = Static(self._spinner.current_frame(), classes="loading-spinner")
            yield self._spinner_widget

            self._status_widget = Static(f" {self._status}... ", classes="loading-status")
            yield self._status_widget

            self._hint_widget = Static("(0s, esc to interrupt)", classes="loading-hint")
            yield self._hint_widget

            # Portal particles inline (subtle, doesn't take extra line)
            self._particles_widget = Static(self._generate_particles(12), classes="loading-particles")
            yield self._particles_widget

    def _generate_particles(self, count: int = 12) -> str:
        """Generate inline portal particles."""
        result = ""
        for _ in range(count):
            if random.random() < 0.4:  # 40% chance for particle
                char = random.choice(PARTICLES)
                color = random.choice(PARTICLE_COLORS)
                result += f"[{color}]{char}[/{color}]"
            else:
                result += " "
        return result

    def on_mount(self) -> None:
        """Start animation on mount."""
        self._start_time = time()
        self.set_interval(0.15, self._update_animation)

    def _update_animation(self) -> None:
        """Update spinner, elapsed time, and particles."""
        if self._paused:
            return

        if self._spinner_widget:
            frame = self._spinner.next_frame()
            self._spinner_widget.update(frame)

        if self._hint_widget and self._start_time is not None:
            elapsed = int(time() - self._start_time)
            self._hint_widget.update(f"({elapsed}s, esc to interrupt)")

        # Update portal particles (inline, subtle)
        if self._particles_widget:
            self._particles_widget.update(self._generate_particles(12))

        # Change the message every ~5 seconds for fun
        self._message_change_counter += 1
        if self._message_change_counter >= 33:  # ~5 seconds at 0.15s interval
            self._message_change_counter = 0
            self._status = random.choice(STRANGER_LOADING_MESSAGES)
            if self._status_widget:
                self._status_widget.update(f" {self._status}... ")

    def set_status(self, status: str) -> None:
        """Update the status text.

        Args:
            status: New status text
        """
        self._status = status
        if self._status_widget:
            self._status_widget.update(f" {self._status}... ")

    def pause(self, status: str = "Awaiting decision from Hawkins Lab") -> None:
        """Pause the animation and update status.

        Args:
            status: Status to show while paused
        """
        self._paused = True
        if self._start_time is not None:
            self._paused_elapsed = int(time() - self._start_time)
        self._status = status
        if self._status_widget:
            self._status_widget.update(f" {status}... ")
        if self._hint_widget:
            self._hint_widget.update(f"(paused at {self._paused_elapsed}s)")
        if self._spinner_widget:
            # Paused state - dim red like a dying Christmas light
            self._spinner_widget.update("[dim #ff0000]◯[/dim #ff0000]")

    def resume(self) -> None:
        """Resume the animation."""
        self._paused = False
        self._status = random.choice(STRANGER_LOADING_MESSAGES)
        if self._status_widget:
            self._status_widget.update(f" {self._status}... ")

    def stop(self) -> None:
        """Stop the animation (widget will be removed by caller)."""
