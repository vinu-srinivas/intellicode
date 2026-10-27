import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

same_preset_problems = []

for p in db["problems"]:
    pid = p["leetcode_id"]
    title = p["title"]
    approaches = p.get("approaches", [])
    primary_app = p.get("primary_approach") or (p.get("primary_solution", {}).get("approach"))
    
    # Simulate frontend brute selection:
    # approaches.find(a => a.name.toLowerCase().includes("brute") || a.name.toLowerCase().includes("naive")) || approaches[0]
    target_brute = next((a for a in approaches if "brute" in a.get("name", "").lower() or "naive" in a.get("name", "").lower()), approaches[0] if approaches else None)
    
    # Simulate frontend optimal selection:
    # approaches.find(a => a.name === problemDetails.primary_approach) || approaches[approaches.length - 1]
    target_opt = next((a for a in approaches if a.get("name") == primary_app), approaches[-1] if approaches else None)
    
    if not target_brute or not target_opt:
        same_preset_problems.append((pid, title, "Missing target approach"))
        continue
        
    for lang in ["python", "java", "cpp"]:
        code_b = target_brute.get("code", {}).get(lang, "").strip()
        code_o = target_opt.get("code", {}).get(lang, "").strip()
        if not code_b or not code_o or code_b == code_o:
            same_preset_problems.append((pid, title, lang, target_brute.get("name"), target_opt.get("name")))
            break

print(f"Total problems where Brute and Optimal presets currently yield identical code: {len(same_preset_problems)}")
for item in same_preset_problems:
    print(" ", item)
