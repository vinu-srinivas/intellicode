import json
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
codebase_path = PROJECT_ROOT / "codebase.json"

with open(codebase_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def fix_python_code(code_str: str) -> str:
    """If code has indentation errors where class Solution has unindented defs/body, fix it."""
    try:
        ast.parse(code_str)
        return code_str
    except Exception:
        pass
        
    lines = code_str.splitlines()
    fixed_lines = []
    in_class = False
    in_def = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            fixed_lines.append("")
            continue
            
        if stripped.startswith("class ") or stripped.startswith("class\t"):
            fixed_lines.append(stripped)
            in_class = True
            in_def = False
        elif stripped.startswith("def "):
            fixed_lines.append("    " + stripped)
            in_def = True
        else:
            if in_def:
                fixed_lines.append("        " + stripped)
            elif in_class:
                fixed_lines.append("    " + stripped)
            else:
                fixed_lines.append(line)
                
    fixed_code = "\n".join(fixed_lines) + "\n"
    try:
        ast.parse(fixed_code)
        return fixed_code
    except Exception as e:
        print(f"Could not automatically fix code:\n{code_str}\nError: {e}")
        return code_str

fixed_count = 0

for p in data["problems"]:
    pid = p["leetcode_id"]
    title = p["title"]
    
    # Check primary
    prim_py = p.get("primary_solution", {}).get("code", {}).get("python", "")
    if prim_py:
        fixed_py = fix_python_code(prim_py)
        if fixed_py != prim_py:
            p["primary_solution"]["code"]["python"] = fixed_py
            fixed_count += 1
            print(f"Fixed primary python for #{pid} {title}")
            
    # Check approaches
    for idx, app in enumerate(p.get("approaches", [])):
        app_py = app.get("code", {}).get("python", "")
        if app_py:
            fixed_py = fix_python_code(app_py)
            if fixed_py != app_py:
                app["code"]["python"] = fixed_py
                fixed_count += 1
                print(f"Fixed approach {idx} ({app.get('name')}) python for #{pid} {title}")

with open(codebase_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully fixed {fixed_count} Python code snippets in codebase.json")
