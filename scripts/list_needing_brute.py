import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db["problems"]:
    pid = p["leetcode_id"]
    title = p["title"]
    category = p["category"]
    primary = p.get("primary_solution", {})
    p_approach = primary.get("approach", "")
    apps = p.get("approaches", [])
    app_names = [a.get("name") for a in apps]
    has_brute = any("brute" in a.lower() for a in app_names)
    if not has_brute or len(apps) <= 1:
        print(f"ID {pid:>3} | {title:<35} | Cat: {category:<20} | Apps: {app_names}")
