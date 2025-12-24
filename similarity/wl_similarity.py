import sys
import math

def read_vec(path):
    with open(path) as f:
        line = f.read().strip()
        if "," in line:
            return [float(x) for x in line.split(",")]
        return [float(x) for x in line.split()]

def cosine(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)

if len(sys.argv) != 3:
    print("Usage: python wl_similarity.py <vec1> <vec2>")
    sys.exit(1)

v1 = read_vec(sys.argv[1])
v2 = read_vec(sys.argv[2])

print(cosine(v1, v2))

