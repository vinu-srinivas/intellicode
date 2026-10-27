import json
import re
import sys
sys.path.insert(0, '.')
from backend.app.curated_brute_codes import CURATED_BRUTE_FORCE

def format_c_code(code: str) -> str:
    """Format Java / C++ code with proper braces and 4-space indentation."""
    if not code:
        return ""
    lines = code.split("\n")
    cleaned_lines = []
    
    for line in lines:
        s = line.strip()
        if not s:
            cleaned_lines.append("")
            continue
        if s.startswith("#") or s.startswith("//") or s.startswith("/*") or s.startswith("*"):
            cleaned_lines.append(s)
            continue
        
        parts = []
        cur = []
        in_paren = 0
        in_str = False
        in_char = False
        escape = False
        
        for ch in s:
            if escape:
                cur.append(ch)
                escape = False
                continue
            if ch == '\\':
                cur.append(ch)
                escape = True
                continue
            if ch == '"' and not in_char:
                in_str = not in_str
                cur.append(ch)
                continue
            if ch == "'" and not in_str:
                in_char = not in_char
                cur.append(ch)
                continue
            if in_str or in_char:
                cur.append(ch)
                continue
                
            if ch == '(':
                in_paren += 1
                cur.append(ch)
            elif ch == ')':
                in_paren -= 1
                cur.append(ch)
            elif ch == '{' and in_paren == 0:
                cur_s = "".join(cur).strip()
                if cur_s:
                    parts.append(cur_s + " {")
                else:
                    parts.append("{")
                cur = []
            elif ch == '}' and in_paren == 0:
                cur_s = "".join(cur).strip()
                if cur_s:
                    parts.append(cur_s)
                parts.append("}")
                cur = []
            elif ch == ';' and in_paren == 0:
                cur.append(ch)
                parts.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
                
        rem = "".join(cur).strip()
        if rem:
            parts.append(rem)
            
        for p in parts:
            if p:
                cleaned_lines.append(p)
                
    expanded = []
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        s = line.strip()
        
        is_control = (
            (s.startswith("if (") or s.startswith("if(") or
             s.startswith("for (") or s.startswith("for(") or
             s.startswith("while (") or s.startswith("while(") or
             s == "else" or s.startswith("else if")) and
            not s.endswith("{") and
            not s.endswith(";")
        )
        
        if is_control and i + 1 < len(cleaned_lines):
            next_line = cleaned_lines[i + 1].strip()
            if next_line == "{":
                expanded.append(s + " {")
                i += 2
                continue
            elif not next_line.startswith("{"):
                expanded.append(s + " {")
                expanded.append(next_line)
                expanded.append("}")
                i += 2
                continue
                
        expanded.append(s)
        i += 1
        
    res = []
    indent = 0
    for line in expanded:
        if not line:
            res.append("")
            continue
        if line.startswith("#"):
            res.append(line)
            continue
            
        if line.startswith("}") or line.startswith("};") or line.startswith("})"):
            indent = max(0, indent - 1)
            
        indent_str = "    " * indent
        if line in ["public:", "private:", "protected:"]:
            res.append("    " + line)
        else:
            res.append(indent_str + line)
            
        if line.endswith("{"):
            indent += 1
            
    return "\n".join(res)

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

updated_brute_count = 0
formatted_langs = 0

for problem in db["problems"]:
    pid = problem["leetcode_id"]
    
    # 1. Check if we have curated brute force for this problem
    if pid in CURATED_BRUTE_FORCE:
        curated_bf = CURATED_BRUTE_FORCE[pid]
        approaches = problem.get("approaches", [])
        
        # Check if approach with "brute" already exists
        bf_idx = -1
        for idx, app in enumerate(approaches):
            if "brute" in app.get("name", "").lower() or "naive" in app.get("name", "").lower():
                bf_idx = idx
                break
                
        new_app = {
            "name": curated_bf["name"],
            "idea": curated_bf["explanation"],
            "complexity": f"Time: {curated_bf['time_complexity']}, Space: {curated_bf['space_complexity']}",
            "explanation": curated_bf["explanation"],
            "code": {
                "python": curated_bf["code"]["python"],
                "java": format_c_code(curated_bf["code"]["java"]),
                "cpp": format_c_code(curated_bf["code"]["cpp"]),
            }
        }
        
        if bf_idx != -1:
            approaches[bf_idx] = new_app
        else:
            approaches.insert(0, new_app)
            
        problem["approaches"] = approaches
        updated_brute_count += 1
        
    # 2. Format all existing Java and C++ codes across all approaches
    for app in problem.get("approaches", []):
        codes = app.get("code", {})
        if "java" in codes and codes["java"]:
            codes["java"] = format_c_code(codes["java"])
            formatted_langs += 1
        if "cpp" in codes and codes["cpp"]:
            codes["cpp"] = format_c_code(codes["cpp"])
            formatted_langs += 1
            
    # Also format primary_solution if present
    prim = problem.get("primary_solution", {})
    prim_codes = prim.get("code", {})
    if "java" in prim_codes and prim_codes["java"]:
        prim_codes["java"] = format_c_code(prim_codes["java"])
    if "cpp" in prim_codes and prim_codes["cpp"]:
        prim_codes["cpp"] = format_c_code(prim_codes["cpp"])

with open("codebase.json", "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Applied curated brute force to {updated_brute_count} problems.")
print(f"Re-formatted {formatted_langs} Java and C++ approach solutions.")
