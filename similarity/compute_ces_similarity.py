import json
from pathlib import Path

VEC_DIR = Path("vectors/ces_norm")
OUT_FILE = Path("evaluation/ces_similarity_matrix.json")
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_vec(p):
    with open(p) as f:
        return [float(x) for x in f.read().strip().split(",")]

def cosine(v1, v2):
    return sum(a*b for a,b in zip(v1,v2))

groups = {}

for v in VEC_DIR.glob("*.norm.vec"):
    name = v.stem.replace(".norm", "")
    parts = name.split("_")
    if len(parts) != 3:
        continue

    problem, role_raw, prog = parts

    # normalize role names
    if role_raw in ("ref", "refs"):
        role = "ref"
    elif role_raw in ("s", "students"):
        role = "s"
    else:
        continue  # unknown role, skip safely

    groups.setdefault(problem, {"ref": [], "s": []})
    groups[problem][role].append(prog)

results = {}

for problem, g in groups.items():
    refs = g["ref"]
    studs = g["s"]
    if not refs or not studs:
        continue

    problem_res = {}

    for s in studs:
        s_vec = load_vec(VEC_DIR / f"{problem}_s_{s}.norm.vec")
        scores = {}

        for r in refs:
            r_vec = load_vec(VEC_DIR / f"{problem}_ref_{r}.norm.vec")
            scores[r] = cosine(r_vec, s_vec)

        problem_res[s] = scores

    results[problem] = problem_res

with open(OUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"[CES] similarity written to {OUT_FILE}")
