  <div align="center">
    <img src="https://github.com/user-attachments/assets/7b0c78cf-7332-4dc3-88f0-cccfd66cb8e1" alt="Stranger Code" width="600" />
  </div>

  <p align="center">
    <img src="https://img.shields.io/badge/python-3.10+-red" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-red" alt="License">
    <img src="https://img.shields.io/badge/vibe-Upside%20Down-darkred" alt="Vibe">
  </p>

  https://github.com/user-attachments/assets/2ed1e621-85d7-417c-b24e-ec0ed83ed735

<p align="center"><strong><em>"Stranger-Code is bitchin." - Eleven probably</em></strong></p>

<p>
  A Stranger Things themed AI coding TUI powered by <a href="https://github.com/langchain-ai/deepagents">deepagents</a>.<br>
  This project basically just adds some fun themes & easter eggs to the great <a href="https://github.com/langchain-ai/deepagents/tree/master/libs/deepagents-cli">deepagents-cli</a>.<br>
  If you want to build something cool like this (or agents generally), check out the deepagents repo!
</p>
---

## Features

- **Joyce's Christmas Lights** - Use `/christmas` to communicate between Hawkins & the Upside Down with lights.
- **Vecna Mode** - Auto-approve for autonomous coding (dangerous!)
- **Upside Down Portal** - Animated splash sequence on startup
- **Mouthbreather Mode** - Manual approval for safety
- **Stranger Things Aesthetic** - Red neon everything

---

## Quick Start

### 1. Set up your API key

```bash
# Pick one (Anthropic is default)
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
export GOOGLE_API_KEY=your_key_here

# Optional: for web search
export TAVILY_API_KEY=your_key_here
```

### 2. Install & Run

```bash
git clone https://github.com/vtrivedy/stranger-code.git
cd stranger-code

# Install with uv (recommended)
uv sync

# Run
uv run stranger-code
```

That's it. The Gate is open.

---

## Usage

```bash
# Normal (with intro sequence)
uv run stranger-code

# Skip the intro
uv run stranger-code --no-splash

# Vecna Mode (auto-approve everything)
uv run stranger-code --auto-approve

# With a specific model
uv run stranger-code --model gpt-4o

# Use a character personality
uv run stranger-code --agent barb
```

---

## Character Agents

Choose your companion from the Stranger Things universe:

| Agent | Personality |
|-------|-------------|
| `--agent barb` | Loyal friend who warns you about bad decisions |
| `--agent eleven` | Few words. Big actions. "Done." |
| `--agent dustin` | Enthusiastic nerd energy, explains everything with excitement |
| `--agent hopper` | Gruff, no BS, "mornings are for coffee and contemplation" |
| `--agent vecna` | Roasts your code with dark elegance |

```bash
# Examples
uv run stranger-code --agent eleven    # Minimal responses, maximum power
uv run stranger-code --agent vecna     # "I have seen your git history... ALL of it."
```

---

## Commands

| Command | What it does |
|---------|--------------|
| `/help` | Show all commands |
| `/clear` | Clear chat, start fresh |
| `/christmas` | Toggle Joyce's Christmas lights |
| `/tokens` | Show token usage |
| `/quit` | Exit the Upside Down |

---

## Modes

| Status Bar | Meaning |
|------------|---------|
| `MOUTHBREATHER (manual)` | You approve each action |
| `VECNA MODE (auto-approve)` | Agent runs autonomously |
| `UPSIDE DOWN (bash)` | Direct shell (type `!command`) |
| `THE VOID (command)` | Slash commands (type `/`) |

Toggle auto-approve anytime with `Shift+Tab`.

---

## How It Works

Stranger Code is built on [deepagents](https://github.com/langchain-ai/deepagents) - check their docs for:
- How the agent architecture works
- Available tools and capabilities
- Advanced configuration options
- Memory and skills system

---

<details>
<summary><strong>Advanced Configuration</strong></summary>


### Agent Memory

Your agent's memory lives in `~/.deepagents/agent/`. Edit `AGENTS.md` there to customize behavior.

</details>

---

## Easter Eggs

There are hidden surprises. Ask the right questions...

---

## Credits

Built on [deepagents](https://github.com/langchain-ai/deepagents) by LangChain.
Stranger Things is a Netflix production. This project is not affiliated with Netflix.

---

> *This repo has escaped Hawkins Lab.*
