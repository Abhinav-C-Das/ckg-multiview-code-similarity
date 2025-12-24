import json
from pathlib import Path

OUT_DIR = Path("vectors/scdps")
VOCAB_FILE = OUT_DIR / "scdps_vocab.json"
SCDPS_ROOT = Path("outputs")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load vocabulary
# --------------------------------------------------
with open(VOCAB_FILE) as f:
    vocab = json.load(f)

dim = len(vocab)

count = 0

# --------------------------------------------------
# Vectorize (EXACTLY like WL)
# --------------------------------------------------
for scdps_file in SCDPS_ROOT.rglob("scdps.json"):
    # outputs/p1/s/s1/scdps.json
    parts = scdps_file.parts

    problem = parts[1]   # p1
    role = parts[2]      # s | ref
    prog = parts[3]      # s1 | ref1

    out_name = f"{problem}_{role}_{prog}.vec"
    out_path = OUT_DIR / out_name

    vec = [0.0] * dim

    with open(scdps_file) as f:
        feats = json.load(f)

    for key, value in feats.items():
        if key in vocab:
            vec[vocab[key]] = float(value)

    with open(out_path, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")

    print(f"[SCDPS] vectorized {out_name}")
    count += 1

print(f"[SCDPS] wrote {count} SCDPS vectors")
