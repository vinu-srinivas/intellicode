import json
import re

with open("codebase.json", "r", encoding="utf-8") as f:
    data = json.load(f)

problems = data["problems"] if "problems" in data else data

print(f"Checking {len(problems)} problems in codebase.json...")

broken_lit_issues = []

for p in problems:
    pid = p.get("leetcode_id", p.get("id"))
    # Check primary solution
    sol = p.get("primary_solution", {})
    code_dict = sol.get("code", {})
    if isinstance(code_dict, dict):
        for lang in ["java", "cpp"]:
            c = code_dict.get(lang, "")
            # Look for unclosed single quotes on a line or broken literals
            for line_no, line in enumerate(c.splitlines(), 1):
                # count unescaped single quotes
                sq = re.findall(r"(?<!\\)'", line)
                if len(sq) % 2 != 0:
                    broken_lit_issues.append((pid, "primary", lang, line_no, line))

    # Check approaches
    for a_idx, app in enumerate(p.get("approaches", [])):
        app_code = app.get("code", {})
        if isinstance(app_code, dict):
            for lang in ["java", "cpp"]:
                c = app_code.get(lang, "")
                for line_no, line in enumerate(c.splitlines(), 1):
                    sq = re.findall(r"(?<!\\)'", line)
                    if len(sq) % 2 != 0:
                        broken_lit_issues.append((pid, f"approach_{a_idx}", lang, line_no, line))

print(f"Found {len(broken_lit_issues)} broken quote lines:")
for issue in broken_lit_issues:
    print(issue)
