"""Status bar widget for Stranger Code - VHS/Hawkins Lab aesthetic."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.app import ComposeResult


class StatusBar(Horizontal):
    """Status bar with VHS-style timestamp and Hawkins Lab mode indicators."""

    DEFAULT_CSS = """
    /* ========================================
       STRANGER CODE STATUS BAR
       VHS Recording Style / Hawkins Lab Console
       ======================================== */

    StatusBar {
        height: 1;
        dock: bottom;
        background: #0a0a0a;
        padding: 0 1;
        color: #6b3a3a;
    }

    StatusBar .status-mode {
        width: auto;
        padding: 0 1;
    }

    StatusBar .status-mode.normal {
        display: none;
    }

    /* BASH mode - Upside-Down (dark, eerie blue-grey) */
    StatusBar .status-mode.bash {
        background: #1a365d;
        color: #90cdf4;
        text-style: bold;
    }

    /* Command mode - Eleven's power blue */
    StatusBar .status-mode.command {
        background: #3d5afe;
        color: #ffffff;
        text-style: bold;
    }

    StatusBar .status-auto-approve {
        width: auto;
        padding: 0 1;
    }

    /* Auto-approve ON - "HAWKINS LAB" - the lab controls everything (red/danger) */
    StatusBar .status-auto-approve.on {
        background: #c53030;
        color: #ffffff;
        text-style: bold;
    }

    /* Auto-approve OFF - "WILL'S HOUSE" - safe space, human oversight */
    StatusBar .status-auto-approve.off {
        background: #2d3748;
        color: #a0aec0;
    }

    StatusBar .status-message {
        width: auto;
        padding: 0 1;
        color: #6b3a3a;
    }

    /* Thinking state - portal opening */
    StatusBar .status-message.thinking {
        color: #ff6b35;
        text-style: italic;
    }

    StatusBar .status-cwd {
        width: 1fr;
        text-align: right;
        color: #4a4a4a;
    }

    /* Token counter - retro green terminal */
    StatusBar .status-tokens {
        width: auto;
        padding: 0 1;
        color: #00ff41;
    }
    """

    mode: reactive[str] = reactive("normal", init=False)
    status_message: reactive[str] = reactive("", init=False)
    auto_approve: reactive[bool] = reactive(default=False, init=False)
    cwd: reactive[str] = reactive("", init=False)
    tokens: reactive[int] = reactive(0, init=False)

    def __init__(self, cwd: str | Path | None = None, **kwargs: Any) -> None:
        """Initialize the status bar.

        Args:
            cwd: Current working directory to display
            **kwargs: Additional arguments passed to parent
        """
        super().__init__(**kwargs)
        # Store initial cwd - will be used in compose()
        self._initial_cwd = str(cwd) if cwd else str(Path.cwd())

    def compose(self) -> ComposeResult:
        """Compose the status bar layout."""
        yield Static("", classes="status-mode normal", id="mode-indicator")
        yield Static(
            "👄 MOUTHBREATHER (manual) | shift+tab",
            classes="status-auto-approve off",
            id="auto-approve-indicator",
        )
        yield Static("", classes="status-message", id="status-message")
        yield Static("", classes="status-tokens", id="tokens-display")
        # CWD shown in welcome banner, not pinned in status bar

    def on_mount(self) -> None:
        """Set reactive values after mount to trigger watchers safely."""
        self.cwd = self._initial_cwd

    def watch_mode(self, mode: str) -> None:
        """Update mode indicator when mode changes."""
        try:
            indicator = self.query_one("#mode-indicator", Static)
        except NoMatches:
            return
        indicator.remove_class("normal", "bash", "command")

        if mode == "bash":
            # Upside-Down mode - direct shell access (dangerous territory!)
            indicator.update("⊥ UPSIDE DOWN (bash)")
            indicator.add_class("bash")
        elif mode == "command":
            # THE VOID - command mode
            indicator.update("◎ THE VOID (command)")
            indicator.add_class("command")
        else:
            indicator.update("")
            indicator.add_class("normal")

    def watch_auto_approve(self, new_value: bool) -> None:  # noqa: FBT001
        """Update auto-approve indicator when state changes."""
        try:
            indicator = self.query_one("#auto-approve-indicator", Static)
        except NoMatches:
            return
        indicator.remove_class("on", "off")

        if new_value:
            # VECNA MODE - auto-approve, he controls everything (danger!)
            indicator.update("☠ VECNA MODE (auto-approve) | shift+tab")
            indicator.add_class("on")
        else:
            # MOUTHBREATHER - manual mode, human approval required
            indicator.update("👄 MOUTHBREATHER (manual) | shift+tab")
            indicator.add_class("off")

    def watch_cwd(self, new_value: str) -> None:
        """Update cwd display when it changes."""
        try:
            display = self.query_one("#cwd-display", Static)
        except NoMatches:
            return
        display.update(self._format_cwd(new_value))

    def watch_status_message(self, new_value: str) -> None:
        """Update status message display."""
        try:
            msg_widget = self.query_one("#status-message", Static)
        except NoMatches:
            return

        msg_widget.remove_class("thinking")
        if new_value:
            msg_widget.update(new_value)
            if "thinking" in new_value.lower() or "executing" in new_value.lower():
                msg_widget.add_class("thinking")
        else:
            msg_widget.update("")

    def _format_cwd(self, cwd_path: str = "") -> str:
        """Format the current working directory for display."""
        path = Path(cwd_path or self.cwd or self._initial_cwd)
        try:
            # Try to use ~ for home directory
            home = Path.home()
            if path.is_relative_to(home):
                return "~/" + str(path.relative_to(home))
        except (ValueError, RuntimeError):
            pass
        return str(path)

    def set_mode(self, mode: str) -> None:
        """Set the current input mode.

        Args:
            mode: One of "normal", "bash", or "command"
        """
        self.mode = mode

    def set_auto_approve(self, *, enabled: bool) -> None:
        """Set the auto-approve state.

        Args:
            enabled: Whether auto-approve is enabled
        """
        self.auto_approve = enabled

    def set_status_message(self, message: str) -> None:
        """Set the status message.

        Args:
            message: Status message to display (empty string to clear)
        """
        self.status_message = message

    def watch_tokens(self, new_value: int) -> None:
        """Update token display when count changes."""
        try:
            display = self.query_one("#tokens-display", Static)
        except NoMatches:
            return

        if new_value > 0:
            # Format with K suffix for thousands
            if new_value >= 1000:
                display.update(f"{new_value / 1000:.1f}K tokens")
            else:
                display.update(f"{new_value} tokens")
        else:
            display.update("")

    def set_tokens(self, count: int) -> None:
        """Set the token count.

        Args:
            count: Current context token count
        """
        self.tokens = count
