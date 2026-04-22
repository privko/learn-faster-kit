#!/usr/bin/env python3
"""
Learn FASTER CLI - One-time installer for OpenCode learning system.

Usage:
    uvx learn-faster init
"""

import sys
import shutil
import platform
import inquirer
import json
from pathlib import Path
from typing import Dict, Any


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


BANNER = f"""{Colors.CYAN}
██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗    ███████╗ █████╗ ███████╗████████╗███████╗██████╗
██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║     █████╗  ███████║██████╔╝██╔██╗ ██║    █████╗  ███████║███████╗   ██║   █████╗  ██████╔╝
██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║    ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
███████╗███████╗██║  ██║██║  ██║██║ ╚████║    ██║     ██║  ██║███████║   ██║   ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}"""


def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message in cyan."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}!{Colors.RESET} {msg}")


def print_header(msg: str) -> None:
    """Print header message in bold magenta."""
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")


def print_dim(msg: str) -> None:
    """Print dimmed message."""
    print(f"{Colors.DIM}{msg}{Colors.RESET}")


def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def get_templates_dir() -> Path:
    """Get the templates directory from the installed package."""
    return Path(__file__).parent.parent / "templates"


def create_opencode_config(project_dir: Path, learning_mode: str) -> None:
    """Create or update opencode.json with Learn FASTER configuration."""
    config_file = project_dir / "opencode.json"

    # Get the path to the system prompt template
    templates_dir = get_templates_dir()
    system_prompt_path = (
        templates_dir / "modes" / learning_mode / "system_prompts" / "learn-faster.md"
    )

    # Default config for Learn FASTER
    default_config = {
        "$schema": "https://opencode.ai/config.json",
        "permission": {
            "bash": {
                "*": "ask",
                "python3 .learning/scripts/*": "allow",
                "ls*": "allow",
                "cat .learning/*": "allow",
            },
            "edit": "allow",
        },
        "agent": {
            "learn-faster": {
                "description": "Learning coach using the FASTER framework",
                "mode": "primary",
                "prompt": f"{{file:{system_prompt_path}}}",
            }
        },
        "default_agent": "learn-faster",
    }

    if config_file.exists():
        # Load existing config
        with open(config_file, "r") as f:
            config = json.load(f)

        # Merge with defaults
        if "permission" not in config:
            config["permission"] = default_config["permission"]
        else:
            # Merge bash permissions
            if "bash" not in config["permission"]:
                config["permission"]["bash"] = {}

            for cmd, perm in default_config["permission"]["bash"].items():
                if cmd not in config["permission"]["bash"]:
                    config["permission"]["bash"][cmd] = perm

        # Add agent config
        if "agent" not in config:
            config["agent"] = {}
        config["agent"]["learn-faster"] = default_config["agent"]["learn-faster"]

        # Set default agent
        config["default_agent"] = "learn-faster"

        print_success(f"Updated {config_file}")
    else:
        # Create new config file
        config = default_config
        print_success(f"Created {config_file}")

    # Write config
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


def check_initialization() -> bool:
    """Check if project has been initialized."""
    config_path = Path.cwd() / ".learning" / "config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("initialized", False)
    except:
        return False


def init_project() -> None:
    """Initialize Learn FASTER in the current project."""

    cwd = Path.cwd()
    templates_dir = get_templates_dir()

    print(BANNER)
    print_header("\nInitializing Learn FASTER in current project...\n")

    # Ask for learning mode selection

    learning_mode_question = [
        inquirer.List(
            "mode",
            message="Choose your learning mode",
            choices=[
                (
                    "Balanced         - Mix of theory, practice, and application",
                    "balanced",
                ),
                (
                    "Exam-Oriented   - Printable exam papers, practice tests, and certification prep",
                    "exam",
                ),
                (
                    "Theory-Focused   - Deep conceptual understanding and mental models",
                    "theory",
                ),
                (
                    "Practical        - Build projects immediately, learn by doing",
                    "practical",
                ),
                (
                    "Programming      - Learn programming through building projects",
                    "programming",
                ),
            ],
            default="balanced",
        ),
    ]

    mode_answer = inquirer.prompt(learning_mode_question)
    learning_mode = mode_answer["mode"] if mode_answer else "balanced"

    mode_names = {
        "exam": "Exam-Oriented",
        "theory": "Theory-Focused",
        "practical": "Practical",
        "balanced": "Balanced",
        "programming": "Programming",
    }
    print_success(f"Selected: {mode_names[learning_mode]} mode\n")

    # Ask about macOS Reminders (only on macOS)
    macos_reminders = False
    if platform.system() == "Darwin":
        response = (
            input(
                f"{Colors.CYAN}Enable macOS Reminders for review notifications? (y/n):{Colors.RESET} "
            )
            .strip()
            .lower()
        )
        macos_reminders = response in ["y", "yes"]

    # Create .opencode directory structure
    opencode_dir = cwd / ".opencode"
    opencode_dir.mkdir(exist_ok=True)

    # Copy mode-specific agents and commands
    mode_templates_dir = templates_dir / "modes" / learning_mode

    # Copy agents for selected mode
    agents_dest = opencode_dir / "agents"
    agents_dest.mkdir(exist_ok=True)
    agents_src = mode_templates_dir / "agents"

    if agents_src.exists():
        for file in agents_src.glob("*.md"):
            shutil.copy2(file, agents_dest / file.name)
            print_success(f"Copied agent: {file.name}")

    # Copy commands for selected mode
    commands_dest = opencode_dir / "commands"
    commands_dest.mkdir(exist_ok=True)
    commands_src = mode_templates_dir / "commands"

    if commands_src.exists():
        for file in commands_src.glob("*.md"):
            shutil.copy2(file, commands_dest / file.name)
            print_success(f"Copied command: {file.name}")

    # Create/update opencode.json
    create_opencode_config(cwd, learning_mode)

    # Create .learning directory structure
    learning_dir = cwd / ".learning"
    learning_dir.mkdir(exist_ok=True)

    # Create config.json with initialization flag
    config = {
        "initialized": True,
        "learning_mode": learning_mode,
        "macos_reminders_enabled": macos_reminders,
    }
    config_path = learning_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print_success(
        f"Created config.json (Mode: {mode_names[learning_mode]}, macOS Reminders: {'enabled' if macos_reminders else 'disabled'})"
    )

    # Copy scripts
    scripts_dest = learning_dir / "scripts"
    scripts_dest.mkdir(exist_ok=True)
    scripts_src = templates_dir / "scripts"
    if scripts_src.exists():
        for file in scripts_src.glob("*.py"):
            shutil.copy2(file, scripts_dest / file.name)
            print_success(f"Copied script: {file.name}")

    # Copy references
    references_dest = learning_dir / "references"
    references_dest.mkdir(exist_ok=True)
    references_src = templates_dir / "references"
    if references_src.exists():
        for file in references_src.glob("*.md"):
            shutil.copy2(file, references_dest / file.name)
            print_success(f"Copied reference: {file.name}")

    # Copy instructions.md to project root as AGENTS.md
    instructions_src = templates_dir / "instructions.md"
    agents_md_dest = cwd / "AGENTS.md"
    if instructions_src.exists() and not agents_md_dest.exists():
        shutil.copy2(instructions_src, agents_md_dest)
        print_success("Copied instructions to AGENTS.md in project root")
    elif agents_md_dest.exists():
        print_warning("AGENTS.md already exists, skipping")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Initialization complete!{Colors.RESET}\n")

    print_header("Available commands in OpenCode:")
    print(
        f"  {Colors.CYAN}/learn [topic]{Colors.RESET}    - Initialize or continue learning"
    )
    print(
        f"  {Colors.CYAN}/review{Colors.RESET}           - Spaced repetition review session"
    )
    print(
        f"  {Colors.CYAN}/progress{Colors.RESET}         - Show detailed progress report"
    )
    print()


def launch_coach(auto_review: bool = False) -> None:
    """Launch OpenCode with learn-faster agent configuration."""
    import subprocess

    # Get the learning mode from config
    config_path = Path.cwd() / ".learning" / "config.json"
    learning_mode = "balanced"  # default
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                learning_mode = config.get("learning_mode", "balanced")
        except:
            pass

    # Verify opencode.json exists with agent config
    opencode_config = Path.cwd() / "opencode.json"
    if not opencode_config.exists():
        print_error("Error: opencode.json not found")
        print_dim("Run 'learn-faster init' to initialize the project")
        sys.exit(1)

    # Launch OpenCode
    print_info("Launching OpenCode in learning coach mode...")
    print_dim("(Using FASTER framework agent)\n")

    # Build command
    cmd = ["opencode"]
    if auto_review:
        cmd.extend(["run", "/review"])

    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print_error("Error: 'opencode' command not found")
        print_dim("Make sure OpenCode CLI is installed and in your PATH")
        print_dim("Install from: https://opencode.ai/docs/#install")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    # Check for explicit commands
    if len(sys.argv) >= 2:
        command = sys.argv[1]

        if command == "init":
            init_project()
            return
        elif command == "version":
            from learn_faster import __version__

            print(f"learn-faster version {__version__}")
            return
        elif command in ["help", "--help", "-h"]:
            print("Learn FASTER - Accelerate learning with FASTER framework\n")
            print("Usage:")
            print(
                "  learn-faster           Auto-init and launch OpenCode in coach mode"
            )
            print("  learn-faster init      Force re-initialization")
            print("  learn-faster version   Show version")
            print()
            print("For more info: https://github.com/cheukyin175/learn-faster-kit")
            return
        else:
            print_error(f"Unknown command: {command}")
            print_dim("Run 'learn-faster --help' for usage")
            sys.exit(1)

    # Default behavior: check init, then launch
    if not check_initialization():
        print_info("First-time setup detected. Initializing...")
        print()
        init_project()
        print()
        print_header("Launching OpenCode with FASTER framework...")
        print()
        launch_coach(auto_review=False)
    else:
        print_info("Launching OpenCode in learning coach mode...")
        print_dim("(Starting with /review to check for due reviews)\n")
        launch_coach(auto_review=True)


if __name__ == "__main__":
    main()
