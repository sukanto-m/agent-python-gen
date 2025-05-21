import os
import json
import re
import time
import subprocess
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import build_python_generation_prompt
from agent.code_executor import run_code_with_tests
from agent.code_explainer import explain_code_with_imports
from agent.utils import clean_code
from agent.docstring_linter import score_docstrings, fix_docstrings
from dashboard import build_dashboard

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")

client = OpenAI(api_key=api_key)

# --- Tool functions ---

def generate_code_task(task_description: str) -> str:
    return build_python_generation_prompt(task_description)

def run_python_code(code: str) -> str:
    stdout, stderr = run_code_with_tests(code)
    if stderr:
        return f"[❌ Tests Failed]\n\n{stderr}"
    return f"[✅ All Tests Passed]\n\n{stdout}"

def save_script_to_file(code: str, task_description: str) -> str:
    safe_name = re.sub(r'\W+', '_', task_description.lower()).strip('_')
    timestamp = int(time.time())
    filename = f"{safe_name[:40]}_{timestamp}.py"
    output_dir = Path("generated_scripts")
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        f.write(code)
    return str(filepath)

def run_script(filepath: str) -> str:
    result = subprocess.run(
        ["python", filepath],
        capture_output=True,
        text=True
    )
    return (result.stdout + result.stderr).strip()

# --- Tool schema definitions for OpenAI ---

tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "generate_code_task",
            "description": "Generate a Python script with functions, tests, and docstrings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "What the user wants the Python script to do"
                    }
                },
                "required": ["task_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Execute a Python script and return test results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python script code to execute with tests"
                    }
                },
                "required": ["code"]
            }
        }
    }
]

# --- Main Agentic Pipeline ---

def stream_python_code_agentic(user_message: str, model: str = "gpt-4") -> Generator[str, None, None]:
    """
    Full agentic pipeline: generates, tests, scores, saves, runs, and explains a Python script.
    Handles tool-calling retries and markdown cleanup.
    """

    # Step 1: Try tool-calling
    planner_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_message}],
        tools=tool_schema,
        tool_choice="auto"
    )
    choice = planner_response.choices[0]

    # Retry if no tool was selected
    if not choice.message.tool_calls:
        yield "[bold yellow]⚠️ Model didn’t select any tool. Retrying with stronger prompt...[/bold yellow]\n"

        retry_messages = [
            {"role": "system", "content": "You must use the available tools to respond to the user query."},
            {"role": "user", "content": user_message}
        ]

        planner_response = client.chat.completions.create(
            model=model,
            messages=retry_messages,
            tools=tool_schema,
            tool_choice="auto"
        )
        choice = planner_response.choices[0]

        if not choice.message.tool_calls:
            yield "[bold red]❌ Retry failed. Model still didn’t use any tool.[/bold red]\n"
            yield f"[bold red]🧾 Raw response:[/bold red] {choice.message.content}\n"
            return

    tool_call = choice.message.tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)
    task_description = function_args["task_description"]

    # Step 2: Generate full Python script
    prompt = generate_code_task(task_description)
    generation_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Python coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw_code = generation_response.choices[0].message.content.strip()
    yield "\n[bold blue]📜 Generated Script:[/bold blue]\n\n"
    yield raw_code + "\n"

    # Step 3: Clean the code (remove backticks)
    cleaned_code = clean_code(raw_code)

    # Step 4: Run tests
    result = run_python_code(cleaned_code)
    yield "\n[bold green]🧪 Test Results:[/bold green]\n\n"
    yield result + "\n"

    # Step 5: Save to file
    filepath = save_script_to_file(cleaned_code, task_description)
    yield f"\n[bold yellow]📁 Script saved to:[/bold yellow] {filepath}\n"

    # Step 6: Run script if tests passed AND no input() calls
    if "[✅" in result:
        if "input(" in cleaned_code:
            yield "\n[bold yellow]⚠️ Script requires user input (input()). Skipping execution to avoid blocking.[/bold yellow]\n"
        else:
            script_output = run_script(filepath)
            yield f"\n[bold green]🚀 Script Execution Output:[/bold green]\n\n{script_output}\n"
    else:
        yield "\n[bold red]❌ Skipping script run due to failed tests.[/bold red]\n"

    # Step 6.1: Update dashboard
    build_dashboard()

    # Step 7: Lint docstrings
    score, warnings = score_docstrings(cleaned_code)
    yield f"\n[bold magenta]📊 Docstring Score: {score}/10[/bold magenta]\n"

    if score < 10:
        yield "[bold red]⚠️ Issues Found:[/bold red]\n" + "\n".join(f"- {w}" for w in warnings) + "\n"
        yield "\n[bold yellow]✍️ Auto-fixing docstrings...[/bold yellow]\n"
        corrected_code = fix_docstrings(cleaned_code)
        corrected_code = clean_code(corrected_code)
        yield "[bold green]✅ Docstrings corrected.[/bold green]\n"

        cleaned_code = corrected_code
        score, _ = score_docstrings(cleaned_code)
        yield f"[bold magenta]📊 New Score: {score}/10[/bold magenta]\n"
    else:
        yield "[bold green]✅ All docstrings look good![/bold green]\n"

    # Step 8: Explain the final version of the code
    yield "\n[bold cyan]💡 Code Explanation:[/bold cyan]\n\n"
    explanation = explain_code_with_imports(cleaned_code)
    yield explanation

    # Step 9: Final message
    yield f"\n[bold green]🎉 Done! Your code is ready at:[/bold green] {filepath}\n"
