Below is a **clean, accurate, paper-grade `README.md`** that reflects **exactly** the project state you reached in this chat — including the fixes, design decisions, and how to run/evaluate everything.

You can drop this directly at the project root.

---

# 📘 Code Similarity via CPG-Based Structural & Semantic Features

This repository implements a **research-grade code similarity and retrieval pipeline** using **Code Property Graphs (CPGs)** built with **Joern 4.x**.
The system extracts **structural**, **semantic**, and **behavioral** features from C programs, converts them into vectors, computes similarity, and evaluates retrieval accuracy against ground truth.

The pipeline is optimized for:

* **Student–reference code comparison**
* **Intra-procedural analysis**
* **Fast, stable execution (no PDG / no full dataflow)**

---

## 🧠 Key Design Decisions (Important)

These are **intentional**, not limitations:

* ❌ **No global PDG / runDataflow**

  * Avoids hangs and huge memory overhead in Joern 4.x
  * Semantic features use **local def–use**, which is sufficient and standard in literature
* ✅ **Intra-procedural def–use only**
* ✅ **Conservative semantic features** (fire only when real semantic patterns exist)
* ✅ **Log-tolerant parsing** (Joern output may contain INFO logs)

This design aligns with **structure-based code assessment models (SBCAM-style systems)**.

---

## 📂 Project Structure

```text
ckg_f2/
│
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
│           └── s_semantic.c   # semantic-rich validation program
│
├── outputs/
│   └── p1/
│       ├── ref/
│       │   └── ref1/
│       │       ├── cpg.bin
│       │       ├── canonical.json
│       │       ├── structural.json
│       │       ├── semantic.json
│       │       ├── behavioral.json
│       │       └── combined_features.json
│       └── s/
│           └── s3/
│               └── (same structure as above)
│
├── vectors/
│   └── baseline/
│       ├── p1_ref_ref1.vec
│       ├── p1_ref_ref1.norm.vec
│       ├── p1_s_s1.vec
│       └── ...
│
├── cpg/
│   └── scripts/
│       ├── preprocess/
│       │   └── canonicalize.sc
│       ├── structural/
│       │   └── basic_structural.sc
│       ├── semantic/
│       │   └── basic_semantic.sc   # FIXED: local def–use (no dataflow)
│       └── behavioral/
│           └── basic_behavioral.sc
│
├── similarity/
│   ├── aggregate_baseline.py
│   ├── vectorize_features.py
│   ├── normalize.py
│   └── similarity.py
│
├── evaluation/
│   ├── similarity_matrix.json
│   ├── ground_truth.json
│   ├── run_similarity_matrix.py
│   └── run_retrieval_evaluation.py
│
├── run_joern.sh
├── run_baseline_pipeline.sh
├── run_full_pipeline.sh
└── README.md
```

---

## 🧩 Feature Extraction

### 1️⃣ Structural Features (`basic_structural.sc`)

Extracted from AST & CFG:

* AST node count
* AST depth (max / average)
* AST node type histogram
* CFG node count
* CFG edge count
* Loop count
* Conditional count

➡ Always available (no dataflow required).

---

### 2️⃣ Semantic Features (`basic_semantic.sc`) **(FIXED)**

Uses **local, intra-procedural def–use only**:

* `def_use_edges`
* `def_use_density`
* `control_predicates`
* `control_data_ratio`
* `param_return_ratio`
* `param_output_ratio`

⚠️ **No `runDataflow()`**

* Prevents hangs
* Prevents memory blowups
* Matches research practice

---

### 3️⃣ Behavioral Features (`basic_behavioral.sc`)

Binary flags:

* `recursion_present`
* `iterative_present`
* `base_case_present`

---

### 4️⃣ Combined Features

Each program produces:

```json
{
  "structural": { ... },
  "semantic": { ... },
  "behavioral": { ... }
}
```

Saved as:

```
outputs/<problem>/<role>/<program>/combined_features.json
```

---

## 🔁 Pipelines

### 🔹 `run_joern.sh`

* Builds CPGs
* Runs canonicalization
* Extracts structural, semantic, behavioral features
* Writes JSON files per program

⚠️ Redirects **stderr**, not stdout, to handle Joern logs safely.

---

### 🔹 `run_baseline_pipeline.sh`

* Aggregates feature JSONs
* Converts them into fixed-length vectors
* Normalizes vectors (L2 / MinMax)
* Stores vectors in `vectors/baseline/`

---

### 🔹 `run_full_pipeline.sh`

Runs **everything end-to-end**:

```bash
./run_joern.sh
./run_baseline_pipeline.sh
```

---

## ▶️ How to Run the Project

### 1️⃣ Prerequisites

* Linux
* Joern 4.x (`joern`, `joern-parse` on PATH)
* Python 3.8+
* `jq`

---

### 2️⃣ Clean Run (Recommended)

```bash
rm -rf outputs vectors
./run_full_pipeline.sh
```

---

### 3️⃣ Inspect Extracted Features

```bash
jq . outputs/p1/s/s3/combined_features.json
```

To inspect raw semantic output (log-tolerant):

```bash
sed -n '/^{/,$p' outputs/p1/s/s_semantic/semantic.json | jq .
```

---

## 📐 Similarity Computation

### 🔹 `similarity/similarity.py`

* Computes cosine similarity
* Feature-aware (structural / semantic / behavioral ranges)
* Outputs:

  * structural similarity
  * semantic similarity
  * behavioral similarity
  * overall similarity

---

### 🔹 Similarity Matrix

```bash
python3 evaluation/run_similarity_matrix.py
```

Produces:

```
evaluation/similarity_matrix.json
```

Format:

```json
{
  "p1": {
    "p1_s_s1": {
      "p1_ref_ref1": { "overall_similarity": 0.82 },
      ...
    }
  }
}
```

---

## 🎯 Evaluation

### Ground Truth

Stored in:

```
evaluation/ground_truth.json
```

Example:

```json
{
  "p1_s1": "p1_ref1",
  "p1_s2": "p1_ref3"
}
```

---

### Retrieval Evaluation

```bash
python3 evaluation/run_retrieval_evaluation.py
```

Outputs:

```json
{
  "accuracy": 0.83,
  "total": 12,
  "correct": 10
}
```

---

## ✅ Validation Performed

* ✔ Structural features vary meaningfully
* ✔ Semantic features fire when appropriate
* ✔ Behavioral flags correct
* ✔ No hangs / no PDG
* ✔ Stable performance
* ✔ Defensible design for publication

---

## 🧠 Final Notes

This pipeline is:

* **Fast**
* **Stable**
* **Explainable**
* **Research-defensible**

It avoids common Joern pitfalls (full dataflow misuse) while still capturing meaningful semantic signal.

---

If you want next:

* feature weighting strategy
* CES integration README
* experiment results template
* paper-ready methodology section

Just say the word.
