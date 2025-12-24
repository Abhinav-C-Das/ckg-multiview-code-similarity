import json
from pathlib import Path

BASELINE_FILE = Path("evaluation/similarity_matrix.json")
WL_FILE = Path("evaluation/wl_similarity_matrix.json")
OUT_FILE = Path("evaluation/combined_similarity.json")

with open(BASELINE_FILE) as f:
    baseline = json.load(f)

with open(WL_FILE) as f:
    wl = json.load(f)

combined = {}

for problem in baseline:
    if problem not in wl:
        continue

    combined[problem] = {}

    for student in baseline[problem]:
        if student not in wl[problem]:
            continue

        combined[problem][student] = {}

        for ref in baseline[problem][student]:
            combined[problem][student][ref] = {
                "baseline": baseline[problem][student].get(ref),
                "wl": wl[problem][student].get(ref)
            }

with open(OUT_FILE, "w") as f:
    json.dump(combined, f, indent=2)

print(f"[AGGREGATE] Combined baseline + WL similarities written to {OUT_FILE}")
