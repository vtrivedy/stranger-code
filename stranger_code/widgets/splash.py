"""Splash screen with Stranger Things intro sequence."""

from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Center
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.message import Message

# Import the EXACT same ASCII from config - includes Rich markup
from stranger_code.config import STRANGER_CODE_ASCII

if TYPE_CHECKING:
    from textual.events import Key


def _strip_markup(text: str) -> str:
    """Remove Rich markup tags from text."""
    return re.sub(r'\[/?[^\]]+\]', '', text)


# Raw text without markup for glitch processing
RAW_TITLE = _strip_markup(STRANGER_CODE_ASCII)

# Glitch characters
GLITCH_CHARS = "▓▒░╬╫╪┼╳※"

# ============================================================================
# VORTEX TRANSITION WITH PARTICLES
# ============================================================================

VORTEX_FRAMES = [
    ("flicker", 6),

    ("vortex", """
    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·
  *    ·  ˚  ·    *    ·  ˚  ·    *    ·  ˚  ·    *    ·  ˚  ·    *    ·  ˚  ·    *
·  ˚     *     ˚  ·  ˚     *     ˚  ·  ˚     *     ˚  ·  ˚     *     ˚  ·  ˚     *
  *   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   *
·     ░░  ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *  ░░     ·
  ˚   ░░ *  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚  ░░   ˚
*     ░░ ·                                                                   ░░     *
  ·   ░░ ˚                                                                   ░░   ·
˚     ░░ *                                                                   ░░     ˚
  *   ░░ ·  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚     *  ˚  ░░   *
·     ░░  *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·  ░░     ·
  ˚   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ˚
*  ˚     ·     ˚  *  ˚     ·     ˚  *  ˚     ·     ˚  *  ˚     ·     ˚  *  ˚     ·
  ·    *  ˚  *    ·    *  ˚  *    ·    *  ˚  *    ·    *  ˚  *    ·    *  ˚  *    ·
    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *    ·    *
"""),

    ("vortex", """
  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·
˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚
  ·  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ·
*    ▒▒  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  ▒▒    *
  ˚  ▒▒ *    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    * ▒▒  ˚
·    ▒▒ ˚    ░░  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  ░░    ˚ ▒▒    ·
  *  ▒▒ ·    ░░ ˚                                                    ˚ ░░    · ▒▒  *
˚    ▒▒ *    ░░ ·                                                    · ░░    * ▒▒    ˚
  ·  ▒▒ ˚    ░░  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ░░    ˚ ▒▒  ·
*    ▒▒ ·    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    · ▒▒    *
  ˚  ▒▒  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ▒▒  ˚
·    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ·
  *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *    ˚    *
˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚
"""),

    ("tunnel", """
·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
˚ ▓▓  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  ▓▓ ˚
  ▓▓ ·  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  · ▓▓
* ▓▓ ˚  ▒▒  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ▒▒  ˚ ▓▓
  ▓▓ *  ▒▒ ˚  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ˚ ▒▒  * ▓▓
· ▓▓ ·  ▒▒ *  ░░            ˚  ·  *  ·  ˚  *  ·  ˚            ░░  * ▒▒  · ▓▓ ·
  ▓▓ ˚  ▒▒ ·  ░░            *  ˚  ·  ˚  *  ·  *  ˚            ░░  · ▒▒  ˚ ▓▓
* ▓▓ *  ▒▒ ˚  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ˚ ▒▒  * ▓▓
  ▓▓ ·  ▒▒  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ▒▒  · ▓▓
˚ ▓▓ ˚  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ˚ ▓▓
  ▓▓  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ▓▓
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
*  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *
"""),

    ("swirl", """
˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚
████████████████████████████████████████████████████████████████████████████████████
██  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ██
██ *  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  * ██
██ ˚  ▓▓  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  ▓▓  ˚ ██
██ ·  ▓▓ ˚  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ˚ ▓▓  · ██
██ *  ▓▓ ·  ▒▒        ˚  *  ·  ████████████  ·  *  ˚        ▒▒  · ▓▓  * ██
██ ˚  ▓▓ *  ▒▒        *  ˚  ·  ████████████  ˚  ·  *        ▒▒  * ▓▓  ˚ ██
██ ·  ▓▓ ˚  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ˚ ▓▓  · ██
██ *  ▓▓  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  ▓▓  * ██
██ ˚  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ˚ ██
██  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ██
████████████████████████████████████████████████████████████████████████████████████
·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·
"""),

    ("swirl", """
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  ████
████ ˚  ██████████████████████████████████████████████████████████████████████  ˚ ████
████ ·  ██  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ██  · ████
████ *  ██ ·  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  · ██  * ████
████ ˚  ██ *  ▓▓            ˚  *  ████████  *  ˚            ▓▓  * ██  ˚ ████
████ ·  ██ ˚  ▓▓            *  ˚  ████████  ˚  *            ▓▓  ˚ ██  · ████
████ *  ██ ·  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  · ██  * ████
████ ˚  ██  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ·  *  ˚  ██  ˚ ████
████ ·  ██████████████████████████████████████████████████████████████████████  · ████
████  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
"""),

    ("dark", """
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ████████████
████████████ *  ██████████████████████████████████████████████████  * ████████████
████████████ ˚  ██          ·  ˚  ████████  ˚  ·          ██  ˚ ████████████
████████████ ·  ██          *  ·  ████████  ·  *          ██  · ████████████
████████████ ˚  ██          ˚  *  ████████  *  ˚          ██  ˚ ████████████
████████████ *  ██████████████████████████████████████████████████  * ████████████
████████████  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  ████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
"""),

    ("dark", """
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
██████████████████████████████████  ˚  *  ██████████████████████████████████████████
██████████████████████████████████  *  ˚  ██████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
"""),

    ("black", """
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████████
"""),

    ("welcome", """




                      ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·



                            W E L C O M E   T O   T H E

                               U P S I D E   D O W N


                      *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *  ·  ˚  *




"""),
]


class SplashComplete(Message):
    """Message sent when splash sequence is complete."""
    pass


class SplashScreen(Widget):
    """Full-screen Stranger Things intro sequence."""

    can_focus = True

    DEFAULT_CSS = """
    SplashScreen {
        width: 100%;
        height: 100%;
        background: #0a0a0a;
        layout: vertical;
        align: center middle;
    }

    SplashScreen Center {
        width: 100%;
        height: auto;
    }

    SplashScreen #title-display {
        width: auto;
        height: auto;
    }

    SplashScreen #prompt-display {
        width: 100%;
        height: auto;
        text-align: center;
        margin-top: 2;
    }

    SplashScreen #sound-cue {
        width: 100%;
        height: auto;
        text-align: center;
        margin-top: 1;
    }
    """

    phase: reactive[str] = reactive("waiting")
    glitch_progress: reactive[float] = reactive(0.0)
    prompt_visible: reactive[bool] = reactive(False)
    prompt_bright: reactive[bool] = reactive(True)
    portal_frame: reactive[int] = reactive(0)

    _glitch_timer = None
    _prompt_timer = None
    _portal_timer = None
    _start_timer = None

    def compose(self) -> ComposeResult:
        yield Center(Static("", id="title-display"))
        yield Static("", id="prompt-display")
        yield Static("", id="sound-cue")

    def on_mount(self) -> None:
        self.focus()
        self._render_glitch_frame()
        self._start_timer = self.set_timer(0.5, self._start_sequence)

    def _start_sequence(self) -> None:
        self.phase = "glitch"
        self._glitch_timer = self.set_interval(0.08, self._advance_glitch)

    def _advance_glitch(self) -> None:
        self.glitch_progress += 0.02
        if self.glitch_progress >= 1.0:
            self._glitch_timer.stop()
            self.phase = "flicker"
            self._do_flicker_sequence()
        else:
            self._render_glitch_frame()

    def _render_glitch_frame(self) -> None:
        title_widget = self.query_one("#title-display", Static)
        glitched = self._apply_glitch(RAW_TITLE, self.glitch_progress)

        if self.glitch_progress < 0.3:
            color = "#4a1a1a"
        elif self.glitch_progress < 0.6:
            color = "#8b2a2a"
        elif self.glitch_progress < 0.8:
            color = "#c41e1e"
        else:
            color = "#e21b1b"

        title_widget.update(f"[bold {color}]{glitched}[/bold {color}]")

    def _apply_glitch(self, text: str, progress: float) -> str:
        result = []
        for char in text:
            if char in " \n":
                result.append(char)
            elif char == "█":
                if random.random() < progress:
                    result.append(char)
                else:
                    result.append(random.choice(GLITCH_CHARS))
            else:
                if random.random() < progress:
                    result.append(char)
                else:
                    result.append(random.choice(GLITCH_CHARS))
        return "".join(result)

    def _do_flicker_sequence(self) -> None:
        flicker_times = [0.0, 0.15, 0.25, 0.35, 0.5]
        states = [True, False, True, False, True]
        for delay, show in zip(flicker_times, states):
            self.set_timer(delay, lambda s=show: self._set_title_visible(s))
        self.set_timer(0.8, self._show_prompt)

    def _set_title_visible(self, visible: bool) -> None:
        title_widget = self.query_one("#title-display", Static)
        if visible:
            # USE STRANGER_CODE_ASCII DIRECTLY - it has Rich markup already!
            title_widget.update(STRANGER_CODE_ASCII)
        else:
            title_widget.update("")

    def _show_prompt(self) -> None:
        self.phase = "prompt"
        self.prompt_visible = True
        self._render_prompt()
        self._prompt_timer = self.set_interval(0.6, self._pulse_prompt)

    def _pulse_prompt(self) -> None:
        self.prompt_bright = not self.prompt_bright
        self._render_prompt()

    def _render_prompt(self) -> None:
        prompt_widget = self.query_one("#prompt-display", Static)
        if not self.prompt_visible:
            prompt_widget.update("")
            return
        if self.prompt_bright:
            prompt_widget.update("[bold #ff1f1f]▸ Press ENTER to open the Gate ◂[/bold #ff1f1f]")
        else:
            prompt_widget.update("[#8b1a1a]▸ Press ENTER to open the Gate ◂[/#8b1a1a]")

    def on_key(self, event: Key) -> None:
        if event.key == "enter" and self.phase == "prompt":
            self._start_portal_transition()
        elif event.key == "escape":
            self._complete_splash()

    def _start_portal_transition(self) -> None:
        self.phase = "portal"
        if self._prompt_timer:
            self._prompt_timer.stop()
        self.prompt_visible = False
        self.query_one("#prompt-display", Static).update("")
        self.portal_frame = 0
        self._flicker_count = 0
        self._welcome_hold = 0
        self._portal_timer = self.set_interval(0.15, self._advance_vortex)

    def _advance_vortex(self) -> None:
        title_widget = self.query_one("#title-display", Static)

        if self.portal_frame >= len(VORTEX_FRAMES):
            self._portal_timer.stop()
            self._complete_splash()
            return

        frame_type, frame_content = VORTEX_FRAMES[self.portal_frame]

        if frame_type == "flicker":
            flicker_count = frame_content
            self._flicker_count += 1
            if self._flicker_count % 2 == 0:
                # USE STRANGER_CODE_ASCII DIRECTLY
                title_widget.update(STRANGER_CODE_ASCII)
            else:
                title_widget.update("")
            if self._flicker_count >= flicker_count:
                self.portal_frame += 1
                self._flicker_count = 0

        elif frame_type == "vortex":
            title_widget.update(f"[#ff3333]{frame_content}[/#ff3333]")
            self.portal_frame += 1

        elif frame_type == "tunnel":
            title_widget.update(f"[#cc0000]{frame_content}[/#cc0000]")
            self.portal_frame += 1

        elif frame_type == "swirl":
            title_widget.update(f"[#990000]{frame_content}[/#990000]")
            self.portal_frame += 1

        elif frame_type == "dark":
            title_widget.update(f"[#330000]{frame_content}[/#330000]")
            self.portal_frame += 1

        elif frame_type == "black":
            title_widget.update(f"[#0a0a0a]{frame_content}[/#0a0a0a]")
            self.portal_frame += 1

        elif frame_type == "welcome":
            # RED with glitch effect that fades out
            if self._welcome_hold < 8:
                # First 8 ticks: glitchy
                glitch_amount = 1.0 - (self._welcome_hold / 8.0)
                glitched = self._apply_glitch(frame_content, 1.0 - glitch_amount * 0.5)
                title_widget.update(f"[bold #ff1f1f]{glitched}[/bold #ff1f1f]")
            else:
                # Rest: stable
                title_widget.update(f"[bold #ff1f1f]{frame_content}[/bold #ff1f1f]")
            self._welcome_hold += 1
            if self._welcome_hold >= 23:
                self.portal_frame += 1

    def _complete_splash(self) -> None:
        if self._glitch_timer:
            self._glitch_timer.stop()
        if self._prompt_timer:
            self._prompt_timer.stop()
        if self._portal_timer:
            self._portal_timer.stop()
        self.post_message(SplashComplete())


class SplashOverlay(Container):
    """Overlay container for the splash screen."""

    DEFAULT_CSS = """
    SplashOverlay {
        width: 100%;
        height: 100%;
        background: #0a0a0a;
        layer: splash;
    }
    """

    def compose(self) -> ComposeResult:
        yield SplashScreen()

    def on_splash_complete(self, event: SplashComplete) -> None:
        self.remove()
