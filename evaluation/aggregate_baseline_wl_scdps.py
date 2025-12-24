import json
from collections import defaultdict

# -----------------------------
# Load inputs
# -----------------------------
baseline = json.load(open("evaluation/similarity_matrix.json"))
wl = json.load(open("evaluation/wl_similarity_matrix.json"))
scdps = json.load(open("evaluation/scdps_similarity_matrix.json"))

final = defaultdict(lambda: defaultdict(dict))

# -----------------------------
# Aggregate per problem
# -----------------------------
for problem in baseline:
    for student in baseline[problem]:
        for ref in baseline[problem][student]:

            entry = {}

            # ---- baseline ----
            entry["baseline"] = baseline[problem][student][ref]

            # ---- WL (CORRECT LOOKUP) ----
            try:
                entry["wl"] = wl[problem][student][ref]
            except KeyError:
                entry["wl"] = 0.0

            # ---- SCDPS (flat matrix) ----
            s_key = f"{problem}_s_{student}.scdps"
            r_key = f"{problem}_ref_{ref}.scdps"

            entry["scdps"] = scdps.get(s_key, {}).get(r_key, 0.0)

            final[problem][student][ref] = entry

# -----------------------------
# Write output
# -----------------------------
with open("evaluation/final_similarity_matrix.json", "w") as f:
    json.dump(final, f, indent=2)

print("[✓] final_similarity_matrix.json written")
