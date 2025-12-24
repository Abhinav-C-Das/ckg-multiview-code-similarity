import json
import subprocess
from pathlib import Path
from collections import defaultdict

VECTORS_DIR = Path("vectors/baseline")
OUT_DIR = Path("evaluation")
OUT_DIR.mkdir(exist_ok=True)

def similarity(ref_id, student_id):
    ref_vec = VECTORS_DIR / f"{ref_id}.norm.vec"
    stu_vec = VECTORS_DIR / f"{student_id}.norm.vec"

    if not ref_vec.exists() or not stu_vec.exists():
        return None

    out = subprocess.check_output(
        ["python3", "similarity/similarity.py", ref_vec, stu_vec],
        text=True
    )
    return json.loads(out)

# --------------------------------------------------
# Discover students and references automatically
# --------------------------------------------------
refs = defaultdict(list)
students = defaultdict(list)

for vec in VECTORS_DIR.glob("*.norm.vec"):
    name = vec.stem.replace(".norm", "")
    parts = name.split("_")

    problem = parts[0]          # p1
    role = parts[1]             # ref or s

    if role == "ref":
        refs[problem].append(name)
    elif role == "s":
        students[problem].append(name)

# --------------------------------------------------
# Compute similarity matrix
# --------------------------------------------------
all_results = {}

for problem in students:
    prob_results = {}

    for stu in students[problem]:
        stu_results = {}

        for ref in refs.get(problem, []):
            sim = similarity(ref, stu)
            if sim is not None:
                stu_results[ref] = sim

        prob_results[stu] = stu_results

    all_results[problem] = prob_results

# --------------------------------------------------
# Write output
# --------------------------------------------------
out_path = OUT_DIR / "similarity_matrix.json"
with open(out_path, "w") as f:
    json.dump(all_results, f, indent=2)

print(f"[OK] Similarity matrix written to {out_path}")
