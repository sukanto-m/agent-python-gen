# agent/code_executor.py

import sys
import io
import traceback
import logging
import ast
from typing import Tuple
from agent.utils import clean_code

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("code_executor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def sanitize_for_exec(code: str) -> str:
    """
    Iteratively drop trailing lines until the code parses as valid Python.
    """
    lines = code.splitlines()
    while lines:
        try:
            ast.parse("\n".join(lines))
            return "\n".join(lines)
        except SyntaxError:
            # Drop the last line and try again
            lines.pop()
    return ""

def run_code_with_tests(code: str) -> Tuple[str, str]:
    """
    Cleans, sanitizes, logs, and executes Python code (with tests).
    Returns (stdout, stderr).
    """
    # 1) Strip fences
    cleaned = clean_code(code)

    # 2) Remove any trailing non-Python lines
    exec_code = sanitize_for_exec(cleaned)

    # 3) Log exactly what we're about to exec()
    logging.debug("==== BEGIN EXECUTING PYTHON CODE ====\n%s\n==== END EXECUTING PYTHON CODE ====", exec_code)

    # 4) Capture stdout and stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

    try:
        exec_globals = {}
        exec(exec_code, exec_globals)
        stdout = sys.stdout.getvalue()
        stderr = sys.stderr.getvalue()
    except Exception:
        stdout = sys.stdout.getvalue()
        stderr = traceback.format_exc()
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

    return stdout.strip(), stderr.strip()