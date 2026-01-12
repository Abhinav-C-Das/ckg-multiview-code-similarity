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
    # NEW structure: outputs/p1/s/s1/ces.json
    # parts = ('p1', 's', 's1', 'ces.json')

    if len(parts) < 4:
        continue

    problem = parts[0]  # p1
    role = parts[1]     # s or ref
    prog = parts[2]     # s1 or ref1
    out_path = VEC_DIR / f"{problem}_{role}_{prog}.vec"

    vec = [0] * len(VOCAB)

    records = load_ces(ces_file)
    for r in records:
        key = f"{r['context']}::{r['evolution']}::{r['operator']}"
        if key in VOCAB:
            vec[VOCAB[key]] += 1

    with open(out_path, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")

print("[CES] vectorization complete")
