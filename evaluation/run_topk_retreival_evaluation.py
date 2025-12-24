import json
from pathlib import Path

SIM_FILE = Path("evaluation/wl_similarity_matrix.json")
GT_FILE = Path("evaluation/ground_truth.json")

TOP_K = [1, 3, 5]

def norm_id(x):
    x = x.replace(".c", "")
    parts = x.split("_")
    return parts[-1]

with open(SIM_FILE) as f:
    sims = json.load(f)

with open(GT_FILE) as f:
    gt_raw = json.load(f)

# --------------------------------------------------
# Normalize ground truth into:
# gt[problem][student] = set(refs)
# --------------------------------------------------
gt = {}

for k, v in gt_raw.items():
    # Case 1: flat mapping "p1_s_s1": ["p1_ref_ref1"]
    if isinstance(v, list) and isinstance(k, str) and "_" in k:
        problem = k.split("_")[0]
        student = norm_id(k)
        refs = {norm_id(x) for x in v}
        gt.setdefault(problem, {})[student] = refs

    # Case 2: problem -> list of [s, r]
    elif isinstance(v, list):
        problem = k
        for pair in v:
            if len(pair) != 2:
                continue
            s, r = pair
            gt.setdefault(problem, {})[norm_id(s)] = {norm_id(r)}

    # Case 3: problem -> dict
    elif isinstance(v, dict):
        problem = k
        for s, refs in v.items():
            if isinstance(refs, list):
                gt.setdefault(problem, {})[norm_id(s)] = {norm_id(x) for x in refs}
            else:
                gt.setdefault(problem, {})[norm_id(s)] = {norm_id(refs)}

# --------------------------------------------------
# Top-k evaluation
# --------------------------------------------------
results = {k: {"correct": 0, "total": 0} for k in TOP_K}

for problem, students in sims.items():
    for student, scores in students.items():
        s_norm = norm_id(student)
        gt_refs = gt.get(problem, {}).get(s_norm, set())

        ranked = sorted(scores.items(), key=lambda x: -x[1])
        ranked_refs = [norm_id(r) for r, _ in ranked]

        for k in TOP_K:
            if set(ranked_refs[:k]) & gt_refs:
                results[k]["correct"] += 1
            results[k]["total"] += 1

print("\nTop-k Retrieval Accuracy:")
for k in TOP_K:
    total = results[k]["total"]
    acc = results[k]["correct"] / total if total else 0.0
    print(f"Top-{k}: {acc:.3f} ({results[k]['correct']}/{total})")
