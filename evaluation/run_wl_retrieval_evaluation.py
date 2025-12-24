import json
from pathlib import Path

SIM_FILE = Path("evaluation/wl_similarity_matrix.json")
GT_FILE = Path("evaluation/ground_truth.json")
OUT_FILE = Path("evaluation/wl_retrieval_results.json")

with open(SIM_FILE) as f:
    sims = json.load(f)

with open(GT_FILE) as f:
    gt = json.load(f)

correct = 0
total = 0

for problem, students in sims.items():
    for student, scores in students.items():
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        top_ref = ranked[0][0]
        if top_ref in gt.get(problem, {}).get(student, []):
            correct += 1
        total += 1

acc = correct / total if total > 0 else 0.0

with open(OUT_FILE, "w") as f:
    json.dump({
        "correct": correct,
        "total": total,
        "accuracy": acc
    }, f, indent=2)

print(f"[WL] retrieval accuracy = {acc:.3f}")
