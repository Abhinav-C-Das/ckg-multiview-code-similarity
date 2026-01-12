import json
import sys
from pathlib import Path

# --------------------------------------------------
# Deterministic baseline feature order (FLAT)
# --------------------------------------------------
FEATURE_ORDER = [
    # Structural
    "ast_node_count",
    "max_ast_depth",
    "avg_ast_depth",
    "cfg_node_count",
    "cfg_edge_count",
    "conditional_count",
    "loop_count",
    "ternary_count",

    # Semantic
    "def_use_edges",
    "def_use_density",
    "control_predicates",
    "control_data_ratio",
    "param_return_ratio",
    "param_output_ratio",

    # Behavioral
    "recursion_present",
    "iterative_present",
    "base_case_present",

    # Variable role / canonicalized features (NEW)
    "var_update_ACCUMULATIVE",
    "var_update_MAX_UPDATE",
    "var_update_MIN_UPDATE",
    "var_update_RECOMPUTED",
    "accumulator_var_count",
    "role_LOOP_INDEX",
    "role_ACCUMULATOR",
    "role_MAX_TRACKER",
    "role_MIN_TRACKER",
    "role_FLAG",
    "role_TEMP",
]

def vectorize(features_path: Path):
    with open(features_path) as f:
        data = json.load(f)

    vector = []
    for key in FEATURE_ORDER:
        value = data.get(key, 0)
        try:
            vector.append(float(value))
        except (TypeError, ValueError):
            vector.append(0.0)

    return vector

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vectorize_features.py <combined_features.json> <output.vec>")
        sys.exit(1)

    features_json = Path(sys.argv[1])
    output_vec = Path(sys.argv[2])

    vec = vectorize(features_json)
    output_vec.parent.mkdir(parents=True, exist_ok=True)

    with open(output_vec, "w") as f:
        f.write(",".join(map(str, vec)) + "\n")
