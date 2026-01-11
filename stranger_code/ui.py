"""UI rendering and display utilities for Stranger Code."""

import json
from pathlib import Path
from typing import Any

from .config import COLORS, STRANGER_CODE_ASCII, MAX_ARG_LENGTH, console


def truncate_value(value: str, max_length: int = MAX_ARG_LENGTH) -> str:
    """Truncate a string value if it exceeds max_length."""
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value


def format_tool_display(tool_name: str, tool_args: dict) -> str:
    """Format tool calls for display with tool-specific smart formatting.

    Shows the most relevant information for each tool type rather than all arguments.

    Args:
        tool_name: Name of the tool being called
        tool_args: Dictionary of tool arguments

    Returns:
        Formatted string for display (e.g., "read_file(config.py)")

    Examples:
        read_file(path="/long/path/file.py") → "read_file(file.py)"
        web_search(query="how to code", max_results=5) → 'web_search("how to code")'
        shell(command="pip install foo") → 'shell("pip install foo")'
    """

    def abbreviate_path(path_str: str, max_length: int = 60) -> str:
        """Abbreviate a file path intelligently - show basename or relative path."""
        try:
            path = Path(path_str)

            # If it's just a filename (no directory parts), return as-is
            if len(path.parts) == 1:
                return path_str

            # Try to get relative path from current working directory
            try:
                rel_path = path.relative_to(Path.cwd())
                rel_str = str(rel_path)
                # Use relative if it's shorter and not too long
                if len(rel_str) < len(path_str) and len(rel_str) <= max_length:
                    return rel_str
            except (ValueError, Exception):
                pass

            # If absolute path is reasonable length, use it
            if len(path_str) <= max_length:
                return path_str

            # Otherwise, just show basename (filename only)
            return path.name
        except Exception:
            # Fallback to original string if any error
            return truncate_value(path_str, max_length)

    # Tool-specific formatting - show the most important argument(s)
    if tool_name in ("read_file", "write_file", "edit_file"):
        # File operations: show the primary file path argument (file_path or path)
        path_value = tool_args.get("file_path")
        if path_value is None:
            path_value = tool_args.get("path")
        if path_value is not None:
            path = abbreviate_path(str(path_value))
            return f"{tool_name}({path})"

    elif tool_name == "web_search":
        # Web search: show the query string
        if "query" in tool_args:
            query = str(tool_args["query"])
            query = truncate_value(query, 100)
            return f'{tool_name}("{query}")'

    elif tool_name == "grep":
        # Grep: show the search pattern
        if "pattern" in tool_args:
            pattern = str(tool_args["pattern"])
            pattern = truncate_value(pattern, 70)
            return f'{tool_name}("{pattern}")'

    elif tool_name == "shell":
        # Shell: show the command being executed
        if "command" in tool_args:
            command = str(tool_args["command"])
            command = truncate_value(command, 120)
            return f'{tool_name}("{command}")'

    elif tool_name == "ls":
        # ls: show directory, or empty if current directory
        if tool_args.get("path"):
            path = abbreviate_path(str(tool_args["path"]))
            return f"{tool_name}({path})"
        return f"{tool_name}()"

    elif tool_name == "glob":
        # Glob: show the pattern
        if "pattern" in tool_args:
            pattern = str(tool_args["pattern"])
            pattern = truncate_value(pattern, 80)
            return f'{tool_name}("{pattern}")'

    elif tool_name == "http_request":
        # HTTP: show method and URL
        parts = []
        if "method" in tool_args:
            parts.append(str(tool_args["method"]).upper())
        if "url" in tool_args:
            url = str(tool_args["url"])
            url = truncate_value(url, 80)
            parts.append(url)
        if parts:
            return f"{tool_name}({' '.join(parts)})"

    elif tool_name == "fetch_url":
        # Fetch URL: show the URL being fetched
        if "url" in tool_args:
            url = str(tool_args["url"])
            url = truncate_value(url, 80)
            return f'{tool_name}("{url}")'

    elif tool_name == "task":
        # Task: show the task description
        if "description" in tool_args:
            desc = str(tool_args["description"])
            desc = truncate_value(desc, 100)
            return f'{tool_name}("{desc}")'

    elif tool_name == "write_todos":
        # Todos: show count of items
        if "todos" in tool_args and isinstance(tool_args["todos"], list):
            count = len(tool_args["todos"])
            return f"{tool_name}({count} items)"

    # Fallback: generic formatting for unknown tools
    # Show all arguments in key=value format
    args_str = ", ".join(f"{k}={truncate_value(str(v), 50)}" for k, v in tool_args.items())
    return f"{tool_name}({args_str})"


def format_tool_message_content(content: Any) -> str:
    """Convert ToolMessage content into a printable string."""
    if content is None:
        return ""
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            else:
                try:
                    parts.append(json.dumps(item))
                except Exception:
                    parts.append(str(item))
        return "\n".join(parts)
    return str(content)


def show_help() -> None:
    """Show help information - Hawkins Lab User Manual."""
    console.print()
    console.print(STRANGER_CODE_ASCII)
    console.print()

    console.print("[bold]Enter the Upside Down:[/bold]", style=COLORS["primary"])
    console.print("  stranger-code [OPTIONS]                        Open the Gate")
    console.print("  stranger-code list                             List all agents in Hawkins")
    console.print("  stranger-code reset --agent AGENT              Reset agent memories")
    console.print(
        "  stranger-code reset --agent AGENT --target SOURCE Copy another agent's powers"
    )
    console.print("  stranger-code help                             Hawkins Lab manual")
    console.print()

    console.print("[bold]Hawkins Lab Configuration:[/bold]", style=COLORS["primary"])
    console.print("  --agent NAME                  Agent codename (default: agent)")
    console.print(
        "  --model MODEL                 AI model (e.g., claude-sonnet-4-5-20250929, gpt-4o)"
    )
    console.print("  --auto-approve                Enable ELEVEN mode (autonomous decisions)")
    console.print(
        "  --sandbox TYPE                Upside Down sandbox (modal, runloop, daytona)"
    )
    console.print("  --sandbox-id ID               Reuse existing portal (skips creation)")
    console.print(
        "  -r, --resume [ID]             Resume session: -r for last, -r <ID> for specific"
    )
    console.print()

    console.print("[bold]Mission Examples:[/bold]", style=COLORS["primary"])
    console.print(
        "  stranger-code                           # Open the Gate", style=COLORS["dim"]
    )
    console.print(
        "  stranger-code --agent eleven            # Use agent 'eleven'",
        style=COLORS["dim"],
    )
    console.print(
        "  stranger-code --model gpt-4o            # Use specific AI powers",
        style=COLORS["dim"],
    )
    console.print(
        "  stranger-code -r                        # Resume last investigation",
        style=COLORS["dim"],
    )
    console.print(
        "  stranger-code -r abc123                 # Resume specific mission",
        style=COLORS["dim"],
    )
    console.print(
        "  stranger-code --auto-approve            # Enable ELEVEN mode",
        style=COLORS["dim"],
    )
    console.print(
        "  stranger-code --sandbox runloop         # Execute in Upside Down sandbox",
        style=COLORS["dim"],
    )
    console.print()

    console.print("[bold]Session Archives:[/bold]", style=COLORS["primary"])
    console.print(
        "  stranger-code threads list              # List all investigations", style=COLORS["dim"]
    )
    console.print(
        "  stranger-code threads delete <ID>       # Close a case", style=COLORS["dim"]
    )
    console.print()

    console.print("[bold]Communication Protocols:[/bold]", style=COLORS["primary"])
    console.print("  Enter           Send transmission", style=COLORS["dim"])
    console.print("  Ctrl+J          Insert newline (like Joyce's lights)", style=COLORS["dim"])
    console.print("  Shift+Tab       Toggle ELEVEN/HAWKINS LAB mode", style=COLORS["dim"])
    console.print("  @filename       Channel file content", style=COLORS["dim"])
    console.print("  /command        Slash commands (/help, /clear, /quit)", style=COLORS["dim"])
    console.print("  !command        Execute Demogorgon shell commands", style=COLORS["dim"])
    console.print()
