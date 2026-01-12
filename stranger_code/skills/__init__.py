"""Skills module - re-exports from deepagents-cli.

Public API:
- SkillsMiddleware: Middleware for integrating skills into agent execution
- execute_skills_command: Execute skills subcommands (list/create/info)
- setup_skills_parser: Setup argparse configuration for skills commands
"""

# Re-export everything from deepagents-cli's skills module
from deepagents_cli.skills import (
    SkillsMiddleware,
    execute_skills_command,
    setup_skills_parser,
)

__all__ = [
    "SkillsMiddleware",
    "execute_skills_command",
    "setup_skills_parser",
]
