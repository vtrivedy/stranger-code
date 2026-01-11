"""Textual widgets for deepagents-cli."""

from __future__ import annotations

from stranger_code.widgets.chat_input import ChatInput
from stranger_code.widgets.messages import (
    AssistantMessage,
    DiffMessage,
    ErrorMessage,
    SystemMessage,
    ToolCallMessage,
    UserMessage,
)
from stranger_code.widgets.status import StatusBar
from stranger_code.widgets.welcome import WelcomeBanner

__all__ = [
    "AssistantMessage",
    "ChatInput",
    "DiffMessage",
    "ErrorMessage",
    "StatusBar",
    "SystemMessage",
    "ToolCallMessage",
    "UserMessage",
    "WelcomeBanner",
]
