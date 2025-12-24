import os
import json
import math

VEC_DIR = "vectors/scdps"
OUT_FILE = "evaluation/scdps_similarity_matrix.json"

def read_vec(path):
    with open(path) as f:
        line = f.read().strip()
        if not line:
            return []
        return [float(x) for x in line.split(",")]

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

vectors = {}

# ---------------------------------------
# LOAD ONLY NORMALIZED VECTORS
# ---------------------------------------
for fname in os.listdir(VEC_DIR):
    if not fname.endswith(".norm.vec"):
        continue

    key = fname.replace(".norm.vec", "")   # clean ID
    vectors[key] = read_vec(os.path.join(VEC_DIR, fname))

results = {}

# ---------------------------------------
# STUDENT → REFERENCE ONLY
# ---------------------------------------
for s in vectors:
    if "_s_" not in s:
        continue

    results[s] = {}

    for r in vectors:
        if "_ref_" not in r:
            continue

        results[s][r] = cosine(vectors[s], vectors[r])

os.makedirs("evaluation", exist_ok=True)
with open(OUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"[SCDPS] Similarity matrix written to {OUT_FILE}")
