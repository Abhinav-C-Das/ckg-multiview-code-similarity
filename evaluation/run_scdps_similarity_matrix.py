import json
import os
import numpy as np

VEC_DIR = "vectors/scdps"
OUT_FILE = "evaluation/scdps_similarity_matrix.json"

vectors = {}
names = []

# --------------------------------------------------
# Load normalized vectors
# --------------------------------------------------
for fname in sorted(os.listdir(VEC_DIR)):
    if not fname.endswith(".norm.vec"):
        continue

    key = fname.replace(".norm.vec", "")
    vec = np.loadtxt(os.path.join(VEC_DIR, fname), delimiter=",")

    vectors[key] = vec
    names.append(key)

# --------------------------------------------------
# Cosine similarity (dot product, already normalized)
# --------------------------------------------------
sim_matrix = {}

for a in names:
    sim_matrix[a] = {}
    va = vectors[a]

    for b in names:
        vb = vectors[b]
        sim_matrix[a][b] = float(np.dot(va, vb))

# --------------------------------------------------
# Write output
# --------------------------------------------------
os.makedirs("evaluation", exist_ok=True)
with open(OUT_FILE, "w") as f:
    json.dump(sim_matrix, f, indent=2)

print(f"[SCDPS EVAL] similarity matrix written to {OUT_FILE}")
