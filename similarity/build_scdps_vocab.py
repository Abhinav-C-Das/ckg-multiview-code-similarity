import json
from pathlib import Path

OUT_DIR = Path("outputs")
VOCAB_OUT = Path("vectors/scdps/scdps_vocab.json")

VOCAB_OUT.parent.mkdir(parents=True, exist_ok=True)

vocab = {}
next_id = 0

# --------------------------------------------------
# Scan all scdps.json files under outputs/
# --------------------------------------------------
for scdps_file in OUT_DIR.rglob("scdps.json"):
    with open(scdps_file) as f:
        data = json.load(f)

    # data is a dict: path_signature -> count
    for key in data.keys():
        if key not in vocab:
            vocab[key] = next_id
            next_id += 1

print(f"[SCDPS] vocab size = {len(vocab)}")

with open(VOCAB_OUT, "w") as f:
    json.dump(vocab, f, indent=2)
