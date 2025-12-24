import json
import os

BASELINE = "evaluation/similarity_matrix.json"
WL = "evaluation/wl_similarity_matrix.json"
SCDPS = "evaluation/scdps_similarity_matrix.json"

OUT = "evaluation/combined_similarity.json"


def load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path) as f:
        return json.load(f)


baseline = load(BASELINE)
wl = load(WL)
scdps = load(SCDPS)

combined = {}

for q in baseline:
    combined[q] = {}
    for c in baseline[q]:
        b = baseline[q][c]

        combined[q][c] = {
            "baseline": {
                "structural": b.get("structural", 0.0),
                "semantic": b.get("semantic", 0.0),
                "behavioral": b.get("behavioral", 0.0),
                "overall": b.get("overall", 0.0)
            },
            "wl": wl.get(q, {}).get(c, 0.0),
            "scdps": scdps.get(q, {}).get(c, 0.0)
        }

with open(OUT, "w") as f:
    json.dump(combined, f, indent=2)

print(f"[AGG] Full-feature similarity written to {OUT}")

