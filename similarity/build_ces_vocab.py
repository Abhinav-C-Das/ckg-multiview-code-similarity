import json
from pathlib import Path
from collections import Counter

OUT_DIR = Path("vectors/ces")
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOCAB_PATH = OUT_DIR / "ces_vocab.json"

vocab = Counter()

for ces_file in Path("outputs").rglob("ces.json"):
    # Skip empty files (valid - means no CES features)
    if ces_file.stat().st_size == 0:
        continue
    
    with open(ces_file) as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError:
            print(f"[WARN] Invalid JSON in {ces_file}, skipping")
            continue
        
        if not records:  # Skip empty lists []
            continue
    for r in records:
        key = f"{r['context']}::{r['evolution']}::{r['operator']}"
        vocab[key] += 1

# Stable index
vocab_index = {k: i for i, k in enumerate(sorted(vocab))}

with open(VOCAB_PATH, "w") as f:
    json.dump(vocab_index, f, indent=2)

print(f"[CES] vocab size = {len(vocab_index)}")
