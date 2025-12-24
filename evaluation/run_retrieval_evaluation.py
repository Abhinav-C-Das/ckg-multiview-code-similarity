import json
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------
SIM_FILE = Path("evaluation/similarity_matrix.json")
GROUND_TRUTH = Path("evaluation/ground_truth.json")

# --------------------------------------------------
# Load inputs
# --------------------------------------------------
with open(SIM_FILE) as f:
    sim_matrix = json.load(f)

with open(GROUND_TRUTH) as f:
    gt = json.load(f)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------
correct = 0
total = 0
results = {}

for student, true_ref in gt.items():
    # student ID format: pX_s_sY
    problem = student.split("_")[0]   # pX

    if problem not in sim_matrix:
        continue

    if student not in sim_matrix[problem]:
        continue

    # -------------------------------
    # USE PRECOMPUTED SIMILARITIES
    # -------------------------------
    scores = {
        ref: sim["overall_similarity"]
        for ref, sim in sim_matrix[problem][student].items()
    }

    if not scores:
        continue

    predicted = max(scores, key=scores.get)
    is_correct = (predicted == true_ref)

    results[student] = {
        "predicted": predicted,
        "ground_truth": true_ref,
        "correct": is_correct,
        "scores": scores
    }

    correct += int(is_correct)
    total += 1

accuracy = correct / total if total > 0 else 0.0

# --------------------------------------------------
# Output
# --------------------------------------------------
print(json.dumps({
    "accuracy": accuracy,
    "total": total,
    "correct": correct,
    "details": results
}, indent=2))
