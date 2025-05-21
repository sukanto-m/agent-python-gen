# agent/prompts.py

def build_python_generation_prompt(task_description: str) -> str:
    """
    Build a prompt that asks the LLM to emit ONLY a standalone Python script,
    with absolutely no Markdown fences (```), no commentary, and no backticks—
    just the raw code.
    """
    return f"""You are a Python coding assistant.

Generate a fully working, standalone Python script that fulfills the following task:

Task:
{task_description}

Guidelines:
- Output ONLY plain Python code. Do NOT wrap it in triple backticks (```) or any Markdown.
- Do NOT include any explanation or comments outside of standard code comments.
- Include all necessary imports.
- Define functions with clean PEP-257 docstrings.
- Add test cases or a main() block at the bottom for demonstration.
- Do NOT append any prose, notes, or instructions—only the code itself.

Begin now, and output nothing but runnable Python.
"""