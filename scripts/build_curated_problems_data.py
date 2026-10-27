import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from data_chunk1 import CHUNK_1
from data_chunk2 import CHUNK_2
from data_chunk3 import CHUNK_3
from data_chunk4 import CHUNK_4
from data_chunk5 import CHUNK_5

all_data = {}
for c in [CHUNK_1, CHUNK_2, CHUNK_3, CHUNK_4, CHUNK_5]:
    all_data.update(c)

out_file = PROJECT_ROOT / "backend" / "app" / "curated_problems_data.py"

with open(out_file, "w", encoding="utf-8") as f:
    f.write('"""\nCurated descriptions, examples, constraints, test cases, and starter codes\nfor all 75 curated DSA problems.\n"""\n\n')
    f.write("CURATED_PROBLEM_EXTRAS = {\n")
    for pid in sorted(all_data.keys()):
        d = all_data[pid]
        f.write(f"    {pid}: {{\n")
        f.write(f"        \"description\": {repr(d['description'])},\n")
        f.write(f"        \"examples\": {repr(d['examples'])},\n")
        f.write(f"        \"constraints\": {repr(d['constraints'])},\n")
        f.write(f"        \"test_cases\": {repr(d['test_cases'])},\n")
        f.write(f"        \"starter_codes\": {repr(d['starter_codes'])},\n")
        f.write("    },\n")
    f.write("}\n")

print(f"Successfully generated {out_file} with {len(all_data)} problems. Size: {out_file.stat().st_size} bytes")
