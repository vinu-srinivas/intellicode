import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

py_errors = 0
brace_errors = 0

for p in db["problems"]:
    pid = p["leetcode_id"]
    for a in p.get("approaches", []):
        aname = a.get("name", "")
        for lang in ["python", "java", "cpp"]:
            code = a.get("code", {}).get(lang, "")
            if lang == "python":
                try:
                    compile(code, f"<p{pid}>", "exec")
                except Exception as e:
                    print(f"Python syntax error in #{pid} {aname}: {e}")
                    py_errors += 1
            else:
                # Check brace balance
                opens = code.count("{")
                closes = code.count("}")
                if opens != closes:
                    print(f"Brace imbalance in #{pid} {aname} ({lang}): opens={opens}, closes={closes}")
                    brace_errors += 1

print(f"Verification complete: {py_errors} Python syntax errors, {brace_errors} Java/C++ brace imbalances.")
