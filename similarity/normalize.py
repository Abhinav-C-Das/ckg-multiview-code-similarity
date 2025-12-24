import sys
import math

def load_vector(path):
    with open(path) as f:
        return [float(x) for x in f.read().strip().split(",")]

def save_vector(vec, path):
    with open(path, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")

def l2_normalize(vec):
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return [0.0 for _ in vec]
    return [x / norm for x in vec]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python normalize.py <input.vec> <output.vec>")
        sys.exit(1)

    inp, out = sys.argv[1], sys.argv[2]
    vec = load_vector(inp)
    norm_vec = l2_normalize(vec)
    save_vector(norm_vec, out)
