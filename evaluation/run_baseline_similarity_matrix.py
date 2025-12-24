import json
from pathlib import Path

VEC_DIR = Path("vectors/baseline")
OUT_FILE = Path("evaluation/similarity_matrix.json")

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Vector utilities
# --------------------------------------------------
def load_vector(path: Path):
    with open(path) as f:
        return [float(x) for x in f.read().strip().split(",")]

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vector length mismatch")
    return sum(a * b for a, b in zip(v1, v2))

# --------------------------------------------------
# Discover vectors
# --------------------------------------------------
groups = {}

for vec in VEC_DIR.glob("*.norm.vec"):
    name = vec.stem.replace(".norm", "")
    parts = name.split("_")
    if len(parts) != 3:
        continue

    problem, role, prog = parts
    groups.setdefault(problem, {"ref": [], "s": []})
    groups[problem][role].append(prog)

# --------------------------------------------------
# Compute similarity matrix
# --------------------------------------------------
results = {}

for problem, g in groups.items():
    refs = g["ref"]
    studs = g["s"]

    if not refs or not studs:
        continue

    problem_res = {}

    for s in studs:
        s_vec_path = VEC_DIR / f"{problem}_s_{s}.norm.vec"
        s_vec = load_vector(s_vec_path)

        scores = {}
        for r in refs:
            r_vec_path = VEC_DIR / f"{problem}_ref_{r}.norm.vec"
            r_vec = load_vector(r_vec_path)

            scores[r] = cosine_similarity(r_vec, s_vec)

        problem_res[s] = scores

    results[problem] = problem_res

# --------------------------------------------------
# Write output
# --------------------------------------------------
with open(OUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"[BASELINE] similarity matrix written to {OUT_FILE}")
