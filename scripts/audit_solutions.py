import json
import sys
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
from app.knowledge_base import load_problems, extract_starter_code

def main():
    problems = load_problems()
    print(f"Loaded {len(problems)} problems.")
    
    py_primary_err = []
    py_approach_err = []
    missing_codes = []
    
    for p in problems:
        pid = p["leetcode_id"]
        title = p["title"]
        
        # Check languages present in primary solution
        prim = p.get("primary_solution", {})
        prim_code = prim.get("code", {})
        for lang in ["python", "java", "cpp"]:
            if not prim_code.get(lang):
                missing_codes.append((pid, title, "primary", lang))
        
        # Check python syntax
        py_code = prim_code.get("python", "")
        if py_code:
            try:
                ast.parse(py_code)
            except Exception as e:
                py_primary_err.append((pid, title, str(e), py_code))
                
        # Check approaches
        for idx, app in enumerate(p.get("approaches", [])):
            app_code = app.get("code", {})
            for lang in ["python", "java", "cpp"]:
                if not app_code.get(lang):
                    missing_codes.append((pid, title, f"approach {idx} ({app.get('name')})", lang))
            py_app = app_code.get("python", "")
            if py_app:
                try:
                    ast.parse(py_app)
                except Exception as e:
                    py_approach_err.append((pid, title, app.get("name"), str(e)))

    print(f"Missing codes: {len(missing_codes)}")
    for m in missing_codes[:20]:
        print(" ", m)
        
    print(f"\nPython primary syntax errors: {len(py_primary_err)}")
    for err in py_primary_err:
        print(f"  #{err[0]} {err[1]}: {err[2]}")
        
    print(f"\nPython approach syntax errors: {len(py_approach_err)}")
    for err in py_approach_err:
        print(f"  #{err[0]} {err[1]} - {err[2]}: {err[3]}")

if __name__ == "__main__":
    main()
