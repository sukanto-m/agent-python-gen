# main.py

import sys
import argparse
from agent.core import stream_python_code_agentic
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

console = Console()


def main():
    """
    Command-line entry point for the Python code generation agent.
    Supports interactive and CLI-based task input, with optional output to file.
    """
    parser = argparse.ArgumentParser(description="Generate Python code using a code agent.")
    parser.add_argument("task", nargs="*", help="Task description for code generation")
    parser.add_argument("--output", "-o", help="Optional output file to save the generated code")

    args = parser.parse_args()
    task = " ".join(args.task) if args.task else Prompt.ask("[bold cyan]Describe the Python task you want to generate[/bold cyan]")

    console.print("\n[bold green]🧠 Python Code Generation Agent[/bold green]")
    console.print("[bold yellow]Generating code... (streaming)[/bold yellow]\n")

    # Stream and display code in ChatGPT-like fashion
    code_lines = []
    for chunk in stream_python_code_agentic(task):
        console.print(chunk, end="")
        code_lines.append(chunk)

    # Save output to file if requested
    if args.output:
        with open(args.output, "w") as f:
            f.write("".join(code_lines))
        console.print(f"\n\n[bold green]✅ Code saved to:[/bold green] {args.output}")


if __name__ == "__main__":
    main()
