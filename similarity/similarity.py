import math
import sys
from pathlib import Path

# Feature index ranges (FROZEN)
STRUCTURAL = range(0, 7)
SEMANTIC   = range(7, 13)
BEHAVIORAL = range(13, 16)

def load_vector(path):
    with open(path) as f:
        return [float(x) for x in f.read().strip().split(",")]

def cosine(v1, v2, idxs):
    a = [v1[i] for i in idxs]
    b = [v2[i] for i in idxs]

    dot = sum(x*y for x, y in zip(a, b))
    na  = math.sqrt(sum(x*x for x in a))
    nb  = math.sqrt(sum(x*x for x in b))

    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python similarity.py <ref.norm.vec> <other.norm.vec>")
        sys.exit(1)

    ref = load_vector(sys.argv[1])
    oth = load_vector(sys.argv[2])

    structural_sim = cosine(ref, oth, STRUCTURAL)
    semantic_sim   = cosine(ref, oth, SEMANTIC)
    behavioral_sim = cosine(ref, oth, BEHAVIORAL)
    overall_sim = ( structural_sim + semantic_sim + behavioral_sim ) / 3.0


    print("{")
    print(f'  "structural_similarity": {structural_sim},')
    print(f'  "semantic_similarity": {semantic_sim},')
    print(f'  "behavioral_similarity": {behavioral_sim},')
    print(f'  "overall_similarity": {overall_sim}')
    print("}")
