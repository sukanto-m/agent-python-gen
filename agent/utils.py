# agent/utils.py

def clean_code(code: str) -> str:
    """
    Remove any Markdown code-fence lines (``` or ```lang) from GPT-generated code.
    """
    cleaned_lines = []
    for line in code.splitlines():
        # Skip lines that start a or end a code fence
        if line.strip().startswith("```"):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)
