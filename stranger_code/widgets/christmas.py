"""Christmas lights widget - Joyce's wall from Stranger Things."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from textual.reactive import reactive
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer

# Joyce's Christmas light colors
LIGHT_COLORS = [
    "#ff0000",  # Red
    "#00ff00",  # Green
    "#0066ff",  # Blue
    "#ffff00",  # Yellow
    "#ff6600",  # Orange
    "#9932cc",  # Purple
]

# Light bulb characters
LIGHT_ON = "●"
LIGHT_DIM = "○"


class ChristmasLights(Static):
    """Animated Christmas lights strip - like Joyce's wall."""

    DEFAULT_CSS = """
    ChristmasLights {
        height: 1;
        width: 100%;
        background: #0a0a0a;
        text-align: center;
    }
    """

    active: reactive[bool] = reactive(False)
    _timer: Timer | None = None
    _frame: int = 0
    _light_count: int = 20

    def __init__(self, light_count: int = 20, **kwargs: Any) -> None:
        """Initialize Christmas lights.

        Args:
            light_count: Number of lights in the string
            **kwargs: Additional arguments passed to parent
        """
        super().__init__("", **kwargs)
        self._light_count = light_count
        self._light_states: list[int] = [0] * light_count  # Color index for each light

    def on_mount(self) -> None:
        """Start animation if active."""
        if self.active:
            self._start_animation()
        else:
            self.display = False

    def watch_active(self, active: bool) -> None:  # noqa: FBT001
        """Start or stop animation when active changes."""
        if active:
            self.display = True
            self._start_animation()
        else:
            self._stop_animation()
            self.display = False

    def _start_animation(self) -> None:
        """Start the lights animation."""
        if self._timer is None:
            # Initialize random light states
            self._light_states = [random.randrange(len(LIGHT_COLORS)) for _ in range(self._light_count)]
            self._render_lights()
            self._timer = self.set_interval(0.3, self._animate_frame)

    def _stop_animation(self) -> None:
        """Stop the lights animation."""
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _animate_frame(self) -> None:
        """Advance animation by one frame."""
        self._frame += 1

        # Randomly flicker some lights (change color or dim)
        for i in range(self._light_count):
            if random.random() < 0.15:  # 15% chance to change each light
                self._light_states[i] = random.randrange(len(LIGHT_COLORS))

        self._render_lights()

    def _render_lights(self) -> None:
        """Render the current lights state."""
        lights_str = ""
        for i, color_idx in enumerate(self._light_states):
            color = LIGHT_COLORS[color_idx]
            # Some lights flicker/dim randomly
            if random.random() < 0.1:
                lights_str += f"[dim {color}]{LIGHT_DIM}[/dim {color}] "
            else:
                lights_str += f"[bold {color}]{LIGHT_ON}[/bold {color}] "

        self.update(lights_str.strip())


class ChristmasMessage(Static):
    """A special Christmas message that appears with the lights."""

    DEFAULT_CSS = """
    ChristmasMessage {
        height: 1;
        width: 100%;
        text-align: center;
        background: #0a0a0a;
    }
    """

    _messages = [
        "R U N",
        "R I G H T   H E R E",
        "H E L L O",
        "C O D E",
    ]

    _timer: Timer | None = None
    _current_msg: int = 0
    _char_idx: int = 0

    def on_mount(self) -> None:
        """Start the message animation."""
        self._render_message()
        self._timer = self.set_interval(0.5, self._advance_char)

    def _advance_char(self) -> None:
        """Advance to next character/message."""
        msg = self._messages[self._current_msg]
        self._char_idx += 1

        if self._char_idx > len(msg):
            # Pause at end of message
            if self._char_idx > len(msg) + 4:
                self._current_msg = (self._current_msg + 1) % len(self._messages)
                self._char_idx = 0

        self._render_message()

    def _render_message(self) -> None:
        """Render the current message state (like Joyce spelling with lights)."""
        msg = self._messages[self._current_msg]
        visible = msg[:self._char_idx]

        # Each character gets a random Christmas color
        colored = ""
        for char in visible:
            if char == " ":
                colored += "  "
            else:
                color = random.choice(LIGHT_COLORS)
                colored += f"[bold {color}]{char}[/bold {color}]"

        self.update(colored)
