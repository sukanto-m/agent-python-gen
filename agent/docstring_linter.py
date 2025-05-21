import ast
from typing import Tuple, List
from agent.utils import clean_code

def score_docstrings(code: str) -> Tuple[int, List[str]]:
    code = clean_code(code)
    total_penalty = 0
    warnings = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return 0, [f"Syntax error while parsing code: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            obj_type = "Function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "Class"
            doc = ast.get_docstring(node)

            if doc is None:
                total_penalty += 3
                warnings.append(f"{obj_type} '{name}' is missing a docstring.")
            else:
                first_line = doc.strip().splitlines()[0] if doc.strip() else ""
                if not first_line:
                    total_penalty += 2
                    warnings.append(f"{obj_type} '{name}' has an empty docstring.")
                else:
                    if not first_line[0].isupper():
                        total_penalty += 1
                        warnings.append(f"{obj_type} '{name}' docstring should start with a capital letter.")
                    if not first_line.endswith("."):
                        total_penalty += 1
                        warnings.append(f"{obj_type} '{name}' docstring should end with a period.")

    score = max(0, 10 - total_penalty)
    return score, warnings

def fix_docstrings(code: str, model="gpt-4") -> str:
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    code = clean_code(code)

    prompt = f"""
Fix only the docstrings in this Python code to follow PEP 257 conventions.
- Use triple double-quoted docstrings.
- First line must be a short summary with capital letter and period.
- Do not change any logic.
- Do not return Markdown formatting like ```.

Code:
{code}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return clean_code(response.choices[0].message.content.strip())
