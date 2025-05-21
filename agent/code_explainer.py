import ast
from typing import List
from agent.utils import clean_code
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_imports(code: str) -> List[str]:
    imports = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])

    return sorted(set(imports))

def get_doc_links(libraries: List[str]) -> List[str]:
    doc_links = {
        "re": "https://docs.python.org/3/library/re.html",
        "math": "https://docs.python.org/3/library/math.html",
        "datetime": "https://docs.python.org/3/library/datetime.html",
        "os": "https://docs.python.org/3/library/os.html",
        "sys": "https://docs.python.org/3/library/sys.html",
        "json": "https://docs.python.org/3/library/json.html",
        "requests": "https://docs.python-requests.org/en/latest/",
        "pandas": "https://pandas.pydata.org/docs/",
        "numpy": "https://numpy.org/doc/",
        "sklearn": "https://scikit-learn.org/stable/documentation.html",
        "matplotlib": "https://matplotlib.org/stable/contents.html",
        "seaborn": "https://seaborn.pydata.org/",
        "openai": "https://platform.openai.com/docs/",
        "torch": "https://pytorch.org/docs/",
        "tensorflow": "https://www.tensorflow.org/api_docs",
        "flask": "https://flask.palletsprojects.com/en/latest/",
        "fastapi": "https://fastapi.tiangolo.com/",
    }

    links = []
    for lib in libraries:
        if lib in doc_links:
            links.append(f"- [{lib}]({doc_links[lib]})")
    return links

def explain_code_with_imports(code: str, model="gpt-4") -> str:
    code = clean_code(code)
    imports = extract_imports(code)
    import_list = ", ".join(imports) if imports else "none"

    prompt = f"""
You are a code explainer.

Here is a Python script. Please:
1. Briefly explain what the code does in plain English.
2. Describe what each of these libraries do in context: [{import_list}]
3. Mention whether the script uses any third-party dependencies.
4. Do NOT repeat the full code.
5. Output plain text only.

Code:
{code}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    explanation = response.choices[0].message.content.strip()
    doc_links = get_doc_links(imports)

    if doc_links:
        explanation += "\n\n📚 Library Documentation Links:\n" + "\n".join(doc_links)

    return explanation
