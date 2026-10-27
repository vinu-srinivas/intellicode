import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print(f"Total problems: {len(db['problems'])}")

same_brute_optimal = []
no_brute = []

for p in db["problems"]:
    pid = p.get("leetcode_id")
    title = p.get("title")
    approaches = p.get("approaches", [])
    approach_names = [a.get("name", "") for a in approaches]
    
    # Check brute force approach
    brute_app = next((a for a in approaches if "brute" in a.get("name", "").lower() or "naive" in a.get("name", "").lower()), None)
    if not brute_app:
        no_brute.append((pid, title, approach_names))
    else:
        # Check optimal
        optimal_app = next((a for a in approaches if a.get("name") == p.get("primary_approach")), approaches[-1] if approaches else None)
        if brute_app == optimal_app or brute_app.get("name") == optimal_app.get("name"):
            same_brute_optimal.append((pid, title, "Same approach object"))
        else:
            # Check if codes are identical
            for lang in ["python", "java", "cpp"]:
                c_brute = brute_app.get("code", {}).get(lang, "").strip()
                c_opt = optimal_app.get("code", {}).get(lang, "").strip()
                if c_brute and c_opt and c_brute == c_opt:
                    same_brute_optimal.append((pid, title, f"Identical code in {lang}"))

print(f"\nProblems with NO approach containing 'brute' or 'naive': {len(no_brute)}")
for pid, title, names in no_brute:
    print(f"  #{pid} {title}: {names}")

print(f"\nProblems where brute and optimal have same approach or identical code: {len(same_brute_optimal)}")
for item in same_brute_optimal:
    print(f"  {item}")
