import json, re

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

unbraced_patterns = []

for p in db["problems"]:
    pid = p["leetcode_id"]
    for a in p.get("approaches", []):
        aname = a.get("name", "")
        for lang in ["java", "cpp"]:
            code = a.get("code", {}).get(lang, "")
            lines = code.split("\n")
            for idx, line in enumerate(lines):
                stripped = line.strip()
                # Check for if/for/while without {
                if (stripped.startswith("if (") or stripped.startswith("for (") or stripped.startswith("while (") or stripped.startswith("for(") or stripped.startswith("while(") or stripped.startswith("if(")):
                    if not stripped.endswith("{") and not stripped.endswith(";"):
                        # next line check
                        if idx + 1 < len(lines):
                            next_line = lines[idx + 1].strip()
                            if next_line != "{":
                                unbraced_patterns.append((pid, p["title"], aname, lang, stripped, next_line))

print(f"Total unbraced if/for/while instances found: {len(unbraced_patterns)}")
for item in unbraced_patterns[:20]:
    print(" ", item)
