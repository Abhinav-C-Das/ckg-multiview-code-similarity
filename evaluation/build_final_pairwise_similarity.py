import json

BASELINE = "evaluation/similarity_matrix.json"
WL = "evaluation/wl_similarity_matrix.json"
SCDPS = "evaluation/scdps_similarity_matrix.json"

OUT = "evaluation/final_similarity_matrix.json"

def load(path):
    with open(path) as f:
        return json.load(f)

baseline = load(BASELINE)
wl = load(WL)
scdps = load(SCDPS)

final = {}

for problem in baseline:
    final[problem] = {}

    for student in baseline[problem]:
        final[problem][student] = {}

        for ref, base_score in baseline[problem][student].items():
            key_student = f"{problem}_s_{student}"
            key_ref = f"{problem}_ref_{ref}"

            wl_score = (
                wl.get(key_student, {}).get(key_ref) or
                wl.get(key_ref, {}).get(key_student) or
                0.0
            )

            scdps_score = (
                scdps.get(f"{key_student}.scdps", {}).get(f"{key_ref}.scdps") or
                scdps.get(f"{key_ref}.scdps", {}).get(f"{key_student}.scdps") or
                0.0
            )

            final[problem][student][ref] = {
                "baseline": base_score,
                "wl": wl_score,
                "scdps": scdps_score
            }

with open(OUT, "w") as f:
    json.dump(final, f, indent=2)

print(f"[FINAL] Pairwise similarity written to {OUT}")
