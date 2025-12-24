import json
import os

BASELINE = "evaluation/similarity_matrix.json"
WL       = "evaluation/wl_similarity_matrix.json"
SCDPS    = "evaluation/scdps_similarity_matrix.json"
CES      = "evaluation/ces_similarity_matrix.json"

OUT = "evaluation/final_similarity_matrix.json"


def load_optional(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


baseline = load_optional(BASELINE)
wl       = load_optional(WL)
scdps    = load_optional(SCDPS)
ces      = load_optional(CES)


def normalize_flat(sim):
    out = {}

    for k, v in sim.items():

        # Already nested
        if isinstance(v, dict) and all(isinstance(x, dict) for x in v.values()):
            problem = k
            out.setdefault(problem, {})
            for student, refs in v.items():
                out[problem].setdefault(student, {})
                for ref, score in refs.items():
                    out[problem][student][ref] = score
            continue

        # Flat format
        if "_" not in k:
            continue

        parts = k.split("_", 2)
        if len(parts) != 3:
            continue

        problem, _, student = parts
        out.setdefault(problem, {}).setdefault(student, {})

        for r_key, score in v.items():
            if "_" not in r_key:
                continue
            r_parts = r_key.split("_", 2)
            if len(r_parts) != 3:
                continue
            ref = r_parts[2]
            out[problem][student][ref] = score

    return out


scdps_n = normalize_flat(scdps)
ces_n   = normalize_flat(ces)


combined = {}

for problem in baseline:
    combined[problem] = {}

    for student in baseline[problem]:
        combined[problem][student] = {}

        for ref in baseline[problem][student]:
            combined[problem][student][ref] = {
                "baseline": baseline[problem][student][ref],
                "wl": wl.get(problem, {}).get(student, {}).get(ref, 0.0),
                "scdps": scdps_n.get(problem, {}).get(student, {}).get(ref, 0.0),
                "ces": ces_n.get(problem, {}).get(student, {}).get(ref, 0.0),
            }

with open(OUT, "w") as f:
    json.dump(combined, f, indent=2)

print(f"[AGG] Final similarity matrix written to {OUT}")
