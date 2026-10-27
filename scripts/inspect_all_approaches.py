import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print(f"Total problems: {len(db['problems'])}")

single_approach = []
no_brute = []

for p in db["problems"]:
    pid = p["leetcode_id"]
    title = p["title"]
    apps = p.get("approaches", [])
    primary = str(p.get("primary_approach") or "")
    has_brute = any("brute" in a.get("name", "").lower() or "naive" in a.get("name", "").lower() for a in apps)
    if len(apps) <= 1:
        single_approach.append((pid, title, [a.get("name") for a in apps]))
    if not has_brute:
        no_brute.append((pid, title, [a.get("name") for a in apps]))
    print(f"#{pid:<4} {title:<40} Approaches: {len(apps):<2} Primary: {primary:<25} HasBrute: {has_brute}")

print(f"\nProblems with only 1 approach: {len(single_approach)}")
for pid, title, apps in single_approach:
    print(f"  #{pid} {title}: {apps}")

print(f"\nTotal problems without an approach explicitly containing 'brute' or 'naive': {len(no_brute)}")
