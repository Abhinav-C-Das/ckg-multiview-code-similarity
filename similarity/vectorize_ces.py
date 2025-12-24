import json
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------
VEC_DIR = Path("vectors/ces")
VEC_DIR.mkdir(parents=True, exist_ok=True)

VOCAB = json.load(open(VEC_DIR / "ces_vocab.json"))
RAW_DIR = Path("outputs")

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def load_ces(path: Path):
    with open(path) as f:
        return json.load(f)

# --------------------------------------------------
# Vectorization
# --------------------------------------------------
for ces_file in RAW_DIR.rglob("ces.json"):
    rel = ces_file.relative_to(RAW_DIR)
    parts = rel.parts
    # examples:
    # outputs/p1_students/s1/ces.json
    # outputs/p1_refs/ref3/ces.json

    if len(parts) < 3:
        continue

    problem_role = parts[0]   # p1_students or p1_refs
    prog = parts[1]           # s1 or ref3

    if "_" not in problem_role:
        continue

    problem, role_raw = problem_role.split("_", 1)

    # -------------------------------
    # Normalize role (CRITICAL)
    # -------------------------------
    if role_raw in ("students", "s"):
        role = "s"
    elif role_raw in ("refs", "ref"):
        role = "ref"
    else:
        continue  # unknown role, skip safely

    out_path = VEC_DIR / f"{problem}_{role}_{prog}.vec"

    vec = [0] * len(VOCAB)

    records = load_ces(ces_file)
    for r in records:
        key = f"{r['context']}::{r['variable']}::{r['evolution']}::{r['operator']}"
        if key in VOCAB:
            vec[VOCAB[key]] += 1

    with open(out_path, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")

print("[CES] vectorization complete")
