import json
from pathlib import Path

OUT_DIR = Path("vectors/wl")
VOCAB_FILE = OUT_DIR / "wl_vocab.json"
WL_ROOT = Path("outputs")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load vocabulary
# --------------------------------------------------
with open(VOCAB_FILE) as f:
    vocab = json.load(f)

dim = len(vocab)

# --------------------------------------------------
# Vectorize
# --------------------------------------------------
count = 0

for wl_file in WL_ROOT.rglob("wl_ast.json"):
    # wl_file = outputs/p1/ref/ref1/wl_ast.json
    parts = wl_file.parts

    problem = parts[1]   # p1
    role = parts[2]      # ref | s
    prog = parts[3]      # ref1 | s1

    out_name = f"{problem}_{role}_{prog}.vec"
    out_path = OUT_DIR / out_name

    vec = [0.0] * dim

    with open(wl_file) as f:
        feats = json.load(f)

    for label, value in feats.items():
        if label in vocab:
            vec[vocab[label]] = float(value)

    with open(out_path, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")

    print(f"[WL] vectorized {out_name}")
    count += 1

print(f"[WL] wrote {count} WL vectors")
