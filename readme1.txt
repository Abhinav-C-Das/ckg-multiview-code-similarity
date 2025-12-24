Good. This is the **right moment to freeze the system** and write the README like a serious research artifact.

Below is a **clean, authoritative README.md** you can drop into the repo **as-is**.
It documents **what exists, why it exists, and how to run everything** without tribal knowledge.

---

# 📘 README — Code Similarity Pipeline (Baseline + WL)

## 1. Project Overview

This project implements a **research-grade code similarity pipeline** for comparing **student solutions against reference solutions**, using:

* **Baseline numeric features** (structural, semantic, behavioral)
* **AST-based Weisfeiler–Lehman (WL) kernel**
* Clean **CPG reuse** via Joern
* **Separated pipelines** for feature extraction, similarity computation, and evaluation
* **Top-k retrieval evaluation** for diagnostic analysis

The design intentionally keeps WL **weak and syntactic**, to motivate stronger semantic representations (e.g., CES).

---

## 2. Directory Structure (Final)

```
ckg_f2/
├── data/
│   └── p1/
│       ├── ref/
│       │   ├── ref1.c
│       │   ├── ref2.c
│       │   └── ref3.c
│       └── s/
│           ├── s1.c
│           ├── s2.c
│           ├── s3.c
│           └── s_semantic.c
│
├── outputs/                         # Joern + feature outputs (CPG reuse)
│   └── p1/ref/ref1/
│       ├── canonical.json
│       ├── structural.json
│       ├── semantic.json
│       ├── behavioral.json
│       └── combined_features.json
│
├── vectors/
│   ├── baseline/
│   │   ├── p1_ref_ref1.vec
│   │   ├── p1_ref_ref1.norm.vec
│   │   └── ...
│   └── wl/
│       ├── wl_vocab.json
│       ├── p1_ref_ref1.vec
│       ├── p1_s_s1.vec
│       └── ...
│
├── cpg/scripts/
│   ├── preprocess/canonicalize.sc
│   ├── structural/basic_structural.sc
│   ├── semantic/basic_semantic.sc
│   ├── behavioral/basic_behavioral.sc
│   └── wl/wl_ast.sc
│
├── similarity/
│   ├── aggregate_baseline.py
│   ├── vectorize_features.py
│   ├── normalize.py
│   ├── build_wl_vocab.py
│   ├── vectorize_wl.py
│   ├── normalize_wl.py
│   ├── wl_similarity.py
│   └── similarity.py
│
├── evaluation/
│   ├── run_baseline_similarity_matrix.py
│   ├── run_wl_similarity_matrix.py
│   ├── aggregate_baseline_wl.py
│   ├── run_topk_retrieval_evaluation.py
│   ├── ground_truth.json
│   ├── similarity_matrix.json
│   ├── wl_similarity_matrix.json
│   └── combined_similarity.json
│
├── experiments/
│   ├── run_joern.sh
│   ├── run_baseline_pipeline.sh
│   └── pipeline/
│       └── run_wl_pipeline.sh
│
├── run_full_pipeline.sh
└── README.md
```

---

## 3. Core Concepts

### Roles

* **ref/** → reference (correct) solutions
* **s/** → student submissions

### Problems

Each subdirectory under `data/` is treated as an **independent problem** (e.g., `p1`, `p2`, …).

### CPG Reuse

* Each program’s CPG is built **once**
* Stored implicitly via Joern execution
* Reused automatically on subsequent runs

---

## 4. Script Responsibilities

### 4.1 Joern / Feature Extraction

#### `experiments/run_joern.sh`

* Builds CPGs using Joern
* Extracts:

  * structural features
  * semantic features (local def–use)
  * behavioral features
* Writes outputs to `outputs/<problem>/<role>/<program>/`
* **Reuses existing CPGs automatically**

Run directly if needed:

```bash
./experiments/run_joern.sh
```

---

### 4.2 Baseline Pipeline

#### `experiments/run_baseline_pipeline.sh`

Per program:

1. Aggregates numeric features (`aggregate_baseline.py`)
2. Vectorizes (`vectorize_features.py`)
3. L2-normalizes (`normalize.py`)
4. Computes baseline similarity matrix

Produces:

```
evaluation/similarity_matrix.json
```

---

#### `evaluation/run_baseline_similarity_matrix.py`

* Computes pairwise similarity between:

  * normalized student vectors
  * normalized reference vectors
* Uses `similarity/similarity.py`
* Output: baseline similarity matrix

---

### 4.3 WL Pipeline

#### `experiments/pipeline/run_wl_pipeline.sh`

Runs the full WL pipeline:

1. WL AST extraction (`wl_ast.sc`)
2. WL vocabulary building
3. WL vectorization
4. WL similarity matrix computation

Produces:

```
evaluation/wl_similarity_matrix.json
```

WL uses:

* L2 normalization (`normalize_wl.py`)
* Cosine similarity (`wl_similarity.py`)
* **AST only (intentionally weak baseline)**

---

### 4.4 Aggregation

#### `evaluation/aggregate_baseline_wl.py`

* Aligns baseline and WL similarities
* Produces a joint view per `(student, reference)`

Output:

```
evaluation/combined_similarity.json
```

Example entry:

```json
{
  "baseline": 0.81,
  "wl": 0.99
}
```

No ranking or evaluation is done here.

---

## 5. Evaluation

### 5.1 Top-k Retrieval Evaluation

#### `evaluation/run_topk_retrieval_evaluation.py`

* Computes Top-k accuracy (k = 1, 3, 5)
* Uses:

  * similarity matrix (WL or baseline)
  * `evaluation/ground_truth.json`
* Normalizes identifiers internally (safe and robust)

Run:

```bash
python3 evaluation/run_topk_retrieval_evaluation.py
```

Expected WL behavior:

* Top-1 ≈ 0
* Top-k may be 0 or >0 depending on ground truth
* This is **diagnostic**, not a failure

---

## 6. Full Pipeline (End-to-End)

### `run_full_pipeline.sh`

Runs everything in correct order:

1. Joern feature extraction (CPG reuse)
2. Baseline pipeline + similarity
3. WL pipeline + similarity
4. Aggregation of baseline + WL

Run:

```bash
./run_full_pipeline.sh
```

After completion, you should have:

```
evaluation/
├── similarity_matrix.json
├── wl_similarity_matrix.json
└── combined_similarity.json
```

---

## 7. Clean Reset (Recommended)

To remove all generated artifacts:

```bash
rm -rf outputs vectors
rm -f evaluation/*similarity*.json
rm -f evaluation/combined_similarity.json
```

Then rerun:

```bash
./run_full_pipeline.sh
```

---

## 8. Design Philosophy (Important)

* **WL is intentionally weak**

  * AST-only
  * No CFG / PDG / canonicalization
* Poor Top-1 accuracy is **expected and meaningful**
* Evaluation is **diagnostic**, not competitive
* Stronger methods (e.g., CES) should clearly outperform both baselines

---

## 9. Extending the System

To add a new method (e.g., CES):

1. Create a pipeline script analogous to `run_wl_pipeline.sh`
2. Produce `evaluation/ces_similarity_matrix.json`
3. Reuse:

   * `aggregate_baseline_wl.py` (extend if needed)
   * `run_topk_retrieval_evaluation.py`

No refactor required.

---

## 10. Final Notes

* Pipelines are **frozen**
* Do not tune WL
* Do not change ground truth
* Focus next on:

  * Top-k plots
  * Comparison tables
  * Experimental section writing

---

If you want, next we can:

* generate plots
* design result tables
* draft the experimental section text

Just say **“move to results”**.
