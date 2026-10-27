# scripts/generate_all_curated_brutes.py
import json

def get_full_brute_codes():
    from backend.app.curated_brute_codes import CURATED_BRUTE_FORCE
    return CURATED_BRUTE_FORCE

print("Testing import...")
d = get_full_brute_codes()
print(f"Already have {len(d)} brute force approaches.")
