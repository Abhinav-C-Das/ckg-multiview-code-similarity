import json
from pathlib import Path
import subprocess

VEC_DIR = Path("vectors/wl")
OUT_FILE = Path("evaluation/wl_similarity_matrix.json")

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def normalize(inp, out):
    subprocess.check_call(
        ["python3", "similarity/normalize_wl.py", str(inp), str(out)]
    )

def similarity(v1, v2):
    out = subprocess.check_output(
        ["python3", "similarity/wl_similarity.py", str(v1), str(v2)]
    )
    return float(out.decode().strip())

# --------------------------------------------------
# Discover ONLY raw WL vectors
# --------------------------------------------------
groups = {}

for vec in VEC_DIR.glob("*.vec"):
    # Ignore derived files
    if vec.name.endswith(".norm.vec"):
        continue

    # Expected: p1_ref_ref1.vec or p1_s_s1.vec
    parts = vec.stem.split("_")
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

    # Normalize refs ONCE
    ref_norm = {}
    for r in refs:
        r_vec = VEC_DIR / f"{problem}_ref_{r}.vec"
        r_norm = VEC_DIR / f"{problem}_ref_{r}.norm.vec"
        normalize(r_vec, r_norm)
        ref_norm[r] = r_norm

    for s in studs:
        s_vec = VEC_DIR / f"{problem}_s_{s}.vec"
        s_norm = VEC_DIR / f"{problem}_s_{s}.norm.vec"
        normalize(s_vec, s_norm)

        scores = {}
        for r in refs:
            scores[r] = similarity(ref_norm[r], s_norm)

        problem_res[s] = scores

    results[problem] = problem_res

with open(OUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"[WL] similarity matrix written to {OUT_FILE}")
