Below is a clean, publication-grade README.md you can drop directly into your repo.
It is written as if an external reviewer / lab mate is reading it and wants to run, inspect, or extend the system.

# Multi-View Code Similarity Pipeline using Joern Code Property Graphs (CPGs)

This repository implements a **research-grade, multi-view code similarity system for C programs** using **Joern CPGs**. 

The system compares **student submissions against reference implementations** using **four orthogonal similarity views**, aggregating them into a final evaluation-ready similarity matrix. Unlike simple token similarity, this system combines **structure, semantics, control/data flow, and variable evolution.**

---

## 🔍 What This Project Does

For each programming problem, the pipeline:
1. **Builds persistent CPGs** (once per program) for efficient reuse.
2. **Extracts multiple feature views**:
   - **Baseline**: Numeric structural and behavioral metrics.
   - **WL (Weisfeiler-Lehman)**: AST kernel features for structural shape.
   - **SCDPS**: Semantic Control-Data Path Signatures (PDG-based paths).
   - **CES**: Computation Evolution Semantics (Variable lifecycle/intent).
3. **Vectorizes and normalizes** each view independently.
4. **Computes Similarity**: Student → Reference cosine similarity for all pairs.
5. **Aggregates**: Late-fusion of all views into a final evaluation matrix.

---

## 📁 Repository Structure

```text
ckg_f5/
├── data/                       # Input C programs (Problem-based)
│   └── p1/
│       ├── ref/                # Reference solutions
│       └── s/                  # Student submissions
├── outputs/                    # Raw extracted features (per program)
├── cpgs/                       # Persistent reusable CPG binaries
├── cpg/scripts/                # Joern Scala (Ocular) scripts
│   ├── preprocess/             # Canonicalization
│   ├── structural/             # AST/CFG metrics
│   ├── semantic/               # Data flow & dependencies
│   ├── behavioral/             # Logic patterns
│   ├── wl/                     # WL Kernel extraction
│   └── scdps/                  # Path signature extraction
├── experiments/                
│   ├── run_joern.sh            # CPG building + baseline extraction
│   └── pipeline/               # Individual view pipelines
├── similarity/                 # Vectorization & math logic
├── evaluation/                 # Aggregation & final JSON matrices
├── run_full_pipeline.sh        # Single-command execution
└── README.md

🧾 Input Data Format
The system expects data organized by Problem ID:

Plaintext

data/p1/
├── ref/
│   ├── ref1.c
│   └── ref2.c
└── s/
    ├── s1.c
    ├── s2.c
    └── s_semantic.c
Comparison Scope: Matches are computed only between submissions in the same problem directory (e.g., s1 vs ref1 within p1).

🧱 Pipeline Overview
0. Clean Reset (Recommended)
Bash

rm -rf outputs vectors evaluation/*.json workspace cpgs features
1. CPG Generation & Baseline Features
Command: bash experiments/run_joern.sh

Builds or reuses cpg.bin.

Runs: canonicalize.sc, basic_structural.sc, basic_semantic.sc, basic_behavioral.sc, and variable_roles.sc.

Output: outputs/p1/s/s1/combined_features.json

2. Baseline Similarity Pipeline
Command: bash experiments/pipeline/run_baseline_pipeline.sh

Vectorizes numeric features and computes student-to-reference cosine similarity.

Output: evaluation/similarity_matrix.json

3. WL (Weisfeiler–Lehman) AST Kernel
Command: bash experiments/pipeline/run_wl_pipeline.sh

Captures AST structural shapes while remaining insensitive to variable renaming.

Output: evaluation/wl_similarity_matrix.json

4. SCDPS (Semantic Control–Data Path Signatures)
Command: bash experiments/pipeline/run_scdps_pipeline.sh

Traverses the Program Dependence Graph (PDG) to find data + control dependency chains.

Output: evaluation/scdps_similarity_matrix.json

5. CES (Computation Evolution Semantics)
Command: bash experiments/pipeline/run_ces_pipeline.sh

Captures how variables evolve (e.g., incrementing in a loop, min/max tracking).

Output: evaluation/ces_similarity_matrix.json

6. Final Aggregation (ALL VIEWS)
Command: python3 evaluation/aggregate_all_features_with_ces.py

Merges all four views into a single structure.

Final Output: evaluation/final_similarity_matrix.json

▶️ Full Pipeline (One Command)
To run the entire system from CPG generation to final aggregation:

Bash

bash run_full_pipeline.sh
🧪 Debugging & Verification
Check extracted features:

Bash

jq . outputs/p1/s/s1/scdps.json
jq . outputs/p1/s/s1/ces.json
Verify vocabulary sizes:

Bash

jq length vectors/scdps/scdps_vocab.json
jq length vectors/wl/wl_vocab.json
Inspect final results:

Bash

jq . evaluation/final_similarity_matrix.json
