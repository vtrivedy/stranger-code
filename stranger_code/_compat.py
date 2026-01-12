"""Compatibility layer for deepagents-cli integration.

This module provides re-exports from deepagents-cli for modules that
stranger-code can share rather than duplicate.

Currently re-exported:
- Shell middleware
- Skills middleware and commands
- Agent memory middleware
- Tools (http_request, fetch_url, web_search)

Stranger-code unique modules (not re-exported):
- config: Stranger Things colors, messages, ASCII art
- app: Textual TUI application
- textual_adapter: Bridges agent to Textual UI
- widgets/: All Textual widgets (splash, christmas, etc.)
- sessions: Thread persistence with SQLite
- main: CLI entry point using Textual app
"""

# Re-export middleware from deepagents-cli
from deepagents_cli.shell import ShellMiddleware
from deepagents_cli.agent_memory import AgentMemoryMiddleware
from deepagents_cli.skills import SkillsMiddleware

# Re-export tools
from deepagents_cli.tools import (
    fetch_url,
    http_request,
    web_search,
)

# Re-export skills commands
from deepagents_cli.skills import (
    execute_skills_command,
    setup_skills_parser,
)

__all__ = [
    # Middleware
    "ShellMiddleware",
    "AgentMemoryMiddleware",
    "SkillsMiddleware",
    # Tools
    "fetch_url",
    "http_request",
    "web_search",
    # Skills commands
    "execute_skills_command",
    "setup_skills_parser",
]
