# dashboard.py

from pathlib import Path

def build_dashboard():
    folder = Path("generated_scripts")
    files = sorted(folder.glob("*.py"), key=lambda f: f.stat().st_mtime, reverse=True)

    html = ["<html><head><title>Generated Scripts</title></head><body>"]
    html.append("<h1>📂 Generated Python Scripts</h1><ul>")

    for f in files:
        html.append(f"<li><a href='{f.name}' target='_blank'>{f.name}</a></li>")

    html.append("</ul></body></html>")

    index_path = folder / "index.html"
    with open(index_path, "w") as file:
        file.write("\n".join(html))

    print(f"✅ Dashboard generated at: {index_path.resolve()}")

if __name__ == "__main__":
    build_dashboard()
