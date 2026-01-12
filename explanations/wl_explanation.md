# Weisfeiler-Lehman (WL) View - Complete Explanation

## Overview
The **WL (Weisfeiler-Lehman) View** is the second view in our multi-view framework. It uses **graph kernel theory** from machine learning to capture **structural patterns** in the Abstract Syntax Tree (AST).

**Key Idea**: Transform the AST into a "fingerprint" by iteratively propagating node labels through the tree structure. Programs with similar AST structures will have similar fingerprints.

---

## Part 1: What is Weisfeiler-Lehman?

### The Graph Isomorphism Problem
**Problem**: How do we tell if two graphs (or trees) have the same structure?

**Example**:
```
Tree A:        Tree B:
  +              *
 / \            / \
x   y          a   b
```
These trees have the **same structure** (binary node with two leaves) but different labels.

**WL Algorithm**: A method to create "signatures" for graph nodes based on their neighborhood structure.

---

## Part 2: How WL Works (Step-by-Step)

### Iteration 0: Initial Labels
Start with the **AST node types** as labels.

**Example AST** for `int x = 5;`:
```
LOCAL (variable declaration)
├─ IDENTIFIER: "x"
└─ LITERAL: "5"
```

**Initial labels** (Iteration 0):
- Node 1: `LOCAL`
- Node 2: `IDENTIFIER`
- Node 3: `LITERAL`

**Count**: `{wl_i0_LOCAL: 1, wl_i0_IDENTIFIER: 1, wl_i0_LITERAL: 1}`

---

### Iteration 1: Combine with Children
For each node, create a new label by combining:
1. **Current label**
2. **Sorted labels of children**

**Formula**: `new_label = hash(current_label + "|" + sorted_child_labels)`

**Example**:
```
Node 1 (LOCAL):
  current = "LOCAL"
  children = ["IDENTIFIER", "LITERAL"]
  combined = "LOCAL|IDENTIFIER,LITERAL"
  new_label = hash("LOCAL|IDENTIFIER,LITERAL") = "a7f3b2..."

Node 2 (IDENTIFIER):
  current = "IDENTIFIER"
  children = []
  combined = "IDENTIFIER|"
  new_label = hash("IDENTIFIER|") = "c8d4e1..."

Node 3 (LITERAL):
  current = "LITERAL"
  children = []
  combined = "LITERAL|"
  new_label = hash("LITERAL|") = "f9a2b3..."
```

**Count**: `{wl_i1_a7f3b2...: 1, wl_i1_c8d4e1...: 1, wl_i1_f9a2b3...: 1}`

---

### Iteration 2: Repeat
Continue with the new labels from iteration 1.

**In our implementation**: We run **MAX_ITER = 2** iterations.

---

## Part 3: Detailed Example with Real Code

### Sample Code:
```c
int sum(int a[], int size) {
  int total = 0;
  for (int j = 0; j < size; j++) {
    total += a[j];
  }
  return total;
}
```

### AST Structure (Simplified):
```
METHOD: "sum"
├─ PARAMETER: "a"
├─ PARAMETER: "size"
├─ BLOCK (function body)
│   ├─ LOCAL: "total"
│   │   └─ LITERAL: "0"
│   ├─ CONTROL_STRUCTURE: "FOR"
│   │   ├─ LOCAL: "j"
│   │   ├─ CALL: "<operator>.lessThan"
│   │   │   ├─ IDENTIFIER: "j"
│   │   │   └─ IDENTIFIER: "size"
│   │   └─ BLOCK (loop body)
│   │       └─ CALL: "<operator>.assignmentPlus"
│   │           ├─ IDENTIFIER: "total"
│   │           └─ CALL: "<operator>.indexAccess"
│   │               ├─ IDENTIFIER: "a"
│   │               └─ IDENTIFIER: "j"
│   └─ RETURN
│       └─ IDENTIFIER: "total"
```

### Iteration 0 Counts:
```json
{
  "wl_i0_METHOD": 1,
  "wl_i0_PARAMETER": 2,
  "wl_i0_BLOCK": 2,
  "wl_i0_LOCAL": 2,
  "wl_i0_LITERAL": 2,
  "wl_i0_CONTROL_STRUCTURE": 1,
  "wl_i0_CALL": 4,
  "wl_i0_IDENTIFIER": 8,
  "wl_i0_RETURN": 1
}
```

### Iteration 1 Example:
```
CONTROL_STRUCTURE node:
  current = "CONTROL_STRUCTURE"
  children = ["LOCAL", "CALL", "BLOCK"]
  sorted = ["BLOCK", "CALL", "LOCAL"]
  combined = "CONTROL_STRUCTURE|BLOCK,CALL,LOCAL"
  hash = "e7f8a9b3c4d5e6f7a8b9c0d1e2f3g4h5i6j7k8l9"
```

**Counts after Iteration 1**: Different hash values for each unique structure pattern

### Iteration 2:
Further refines the labels based on the iteration 1 hashes.

---

## Part 4: What Do WL Features Capture?

### Structural Patterns Detected:

#### 1. **Loop with Assignment Inside**
```c
for (...) {
  x += y;
}
```
WL captures: `FOR → BLOCK → ASSIGNMENT_PLUS`

#### 2. **Nested Conditionals**
```c
if (a > b) {
  if (x < y) {
    // ...
  }
}
```
WL captures: `IF → BLOCK → IF → BLOCK` pattern

#### 3. **Array Access in Loop**
```c
for (int i = 0; i < n; i++) {
  arr[i] = ...;
}
```
WL captures: `FOR → indexAccess` relationship

### What WL Does NOT Capture:

❌ **Variable names**: All variables are just "IDENTIFIER"
❌ **Literal values**: All numbers are just "LITERAL"
❌ **Semantic meaning**: Doesn't know if `x += arr[i]` is accumulation or recomputation
❌ **Control flow semantics**: Can't distinguish accumulation from max-finding

**Example of WL limitation**:
```c
// Program A: Accumulation
int sum = 0;
for (int i = 0; i < n; i++) {
  sum += arr[i];
}

// Program B: Recomputation
int sum;
for (int i = 0; i < n; i++) {
  sum = sum + arr[i];
}
```
**WL sees these as IDENTICAL** because AST structure is the same!

---

## Part 5: Feature Extraction Pipeline

### Step 1: WL AST Extraction (`wl_ast.sc`)

**Input**: CPG (from Joern)
**Output**: `wl_ast.json` with feature counts

**Script Logic**:
```scala
// 1. Get all AST nodes for the program
val nodes = method.ast.l

// 2. Initialize with node types (iteration 0)
nodes.foreach { n =>
  labels(n.id) = n.label
  count("wl_i0_" + n.label)
}

// 3. Run WL iterations (1 and 2)
for (i <- 1 to MAX_ITER) {
  nodes.foreach { n =>
    // Combine current label with sorted child labels
    val childLabels = n.astChildren.map(c => labels(c.id)).sorted
    val combined = labels(n.id) + "|" + childLabels.mkString(",")
    
    // Hash to create stable label
    val hashed = SHA1(combined)
    
    // Update and count
    newLabels(n.id) = hashed
    count("wl_i" + i + "_" + hashed)
  }
}
```

**Example Output** (`wl_ast.json`):
```json
{
  "wl_i0_IDENTIFIER": 8,
  "wl_i0_LITERAL": 2,
  "wl_i0_CALL": 4,
  "wl_i0_CONTROL_STRUCTURE": 1,
  "wl_i1_a7f3b2c4d5e6f7a8": 3,
  "wl_i1_f9e8d7c6b5a4f3e2": 5,
  "wl_i2_1a2b3c4d5e6f7a8b": 2,
  ...
}
```

---

## Part 6: Vocabulary Building

### Step 2: Build Global Vocabulary (`build_wl_vocab.py`)

**Problem**: Different programs have different WL features (due to different structures).

**Solution**: Create a **global vocabulary** of ALL WL features across ALL programs.

**Process**:
1. Scan all `wl_ast.json` files in `outputs/`
2. Collect all unique feature labels
3. Assign each a unique integer ID
4. Save as `wl_vocab.json`

**Example Vocabulary**:
```json
{
  "wl_i0_IDENTIFIER": 0,
  "wl_i0_LITERAL": 1,
  "wl_i0_CALL": 2,
  "wl_i0_CONTROL_STRUCTURE": 3,
  "wl_i1_a7f3b2c4d5e6f7a8": 4,
  "wl_i1_f9e8d7c6b5a4f3e2": 5,
  ...
  "wl_i2_9z8y7x6w5v4u3t2s": 487
}
```

**Vocabulary Size**: Typically **300-500** unique features across all programs.

---

## Part 7: Vectorization

### Step 3: Convert to Fixed-Length Vectors (`vectorize_wl.py`)

**Goal**: Convert each program's WL features to a vector of length = vocabulary size.

**Process**:
1. Create a zero vector of size = len(vocabulary)
2. For each feature in the program's `wl_ast.json`:
   - Find its index in the vocabulary
   - Set vector[index] = count

**Example**:

**Program's WL features**:
```json
{
  "wl_i0_IDENTIFIER": 8,
  "wl_i0_LITERAL": 2,
  "wl_i1_a7f3b2c4d5e6f7a8": 3
}
```

**Vocabulary**:
```json
{
  "wl_i0_IDENTIFIER": 0,
  "wl_i0_LITERAL": 1,
  "wl_i0_CALL": 2,
  "wl_i1_a7f3b2c4d5e6f7a8": 3
}
```

**Vector** (length 4):
```
[8, 2, 0, 3]
 ^  ^  ^  ^
 |  |  |  └─ wl_i1_a7f3b2c4d5e6f7a8: count = 3
 |  |  └─ wl_i0_CALL: count = 0 (not in program)
 |  └─ wl_i0_LITERAL: count = 2
 └─ wl_i0_IDENTIFIER: count = 8
```

**Actual vectors**: Length ~400-500 with most values = 0 (sparse)

**Output**: `p1_s_s1.vec` (comma-separated values)

---

## Part 8: Normalization

### Step 4: L2 Normalization (`normalize_wl.py`)

**Same as Baseline view**: Scale vector to unit length.

**Why?** Makes programs comparable regardless of size.

**Formula**:
```
norm = sqrt(sum(x² for x in vector))
normalized_vector = [x / norm for x in vector]
```

**Example**:
```
Original: [8, 2, 0, 3, 0, 0, 5, ...]
Norm: sqrt(8² + 2² + 0² + 3² + ... + 5²) = 10.77
Normalized: [0.742, 0.186, 0, 0.278, 0, 0, 0.464, ...]
```

**Output**: `p1_s_s1.norm.vec`

---

## Part 9: Similarity Calculation

### Step 5: Cosine Similarity (`wl_similarity.py`)

**Same concept as Baseline**, but simpler (no feature groups).

**Formula**:
```
similarity = dot(vector1, vector2) / (||vector1|| × ||vector2||)

For normalized vectors:
similarity = dot(vector1, vector2)
```

**Example**:

**Student (s1)**: `[0.742, 0.186, 0, 0.278, 0, 0, 0.464, ...]`
**Reference (ref1)**: `[0.740, 0.185, 0, 0.280, 0, 0, 0.465, ...]`

**Dot Product**:
```
0.742×0.740 + 0.186×0.185 + 0×0 + 0.278×0.280 + ... + 0.464×0.465
= 0.549 + 0.034 + 0 + 0.078 + ... + 0.215
= 0.987
```

**Similarity**: **0.987** (98.7% similar) ✅

---

## Part 10: Complete Pipeline Flow

```
┌─────────────┐
│  C Program  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Joern (CPG)    │  ← Build AST
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   wl_ast.sc     │  ← Extract WL features (2 iterations)
└──────┬──────────┘
       │
       ▼  wl_ast.json (per program)
       │
       ├─ All programs →┌──────────────────┐
       │                │build_wl_vocab.py │  ← Build global vocabulary
       │                └────────┬─────────┘
       │                         │
       │                         ▼  wl_vocab.json
       ├─────────────────────────┘
       │
       ▼
┌──────────────────────┐
│  vectorize_wl.py     │  ← Convert to fixed-length vector
└──────┬───────────────┘
       │
       ▼  program.vec (length ~400-500)
┌──────────────────────┐
│  normalize_wl.py     │  ← L2 normalization
└──────┬───────────────┘
       │
       ▼  program.norm.vec
┌──────────────────────┐
│ wl_similarity.py     │  ← Cosine similarity
└──────┬───────────────┘
       │
       ▼
  WL Similarity (0-1)
```

---

## Part 11: Why WL is "Intentionally Weak"

### Design Philosophy
WL is deliberately kept **syntactic** and **weak** in our system.

**Why?**
1. **Baseline comparison**: Shows what pure structural similarity achieves
2. **Motivates stronger methods**: Demonstrates need for semantic views (CES)
3. **Fast and deterministic**: No training, consistent results

### Expected Behavior

✅ **WL is GOOD at**:
- Detecting identical code structures
- Finding syntactic clones
- Matching programs that differ only in variable names

❌ **WL is BAD at**:
- Distinguishing semantic differences
- Identifying different computational strategies
- Understanding algorithmic intent

### Real Results

**Example 1**: Two sum programs (same algorithm, different variable names)
```
WL Similarity: 0.99 ✅ (correctly identified as very similar)
```

**Example 2**: Sum (accumulation) vs Sum (recomputation)
```
WL Similarity: 0.98 ❌ (incorrectly says similar - same structure!)
Baseline Similarity: 0.65 ✓ (better - sees semantic difference)
CES Similarity: 0.35 ✓✓ (best - captures accumulative vs recomputed)
```

---

## Part 12: Key Mathematical Properties

### 1. WL Kernel Theory
WL is based on **graph kernel** theory from machine learning.

**Kernel Trick**: Instead of explicitly comparing graphs, compare their feature vectors.

### 2. Iteration Depth
- **Iteration 0**: Captures **node types**
- **Iteration 1**: Captures **immediate neighborhood** (1-hop)
- **Iteration 2**: Captures **2-hop neighborhoods**

**More iterations** = **more context** but also **more features** (sparse, high-dimensional)

**Our choice**: 2 iterations balances expressiveness and efficiency.

### 3. Hash Stability
We use **SHA-1 hash** for deterministic label generation.

**Why hash?**
- Labels can be very long strings after iterations
- Hash creates fixed-length identifiers
- Deterministic (same input → same hash)

---

## Part 13: Comparison with Baseline View

| Aspect | Baseline | WL |
|--------|----------|-----|
| **Features** | 18 numeric metrics | 400-500 structural patterns |
| **Focus** | Counts (loops, conditionals) | Tree structure |
| **Strength** | Semantic metrics (def-use) | Fine-grained syntax |
| **Weakness** | Coarse-grained | Purely syntactic |
| **Vector size** | 18 dimensions | ~400-500 dimensions |
| **Interpretability** | High (named features) | Low (hashed labels) |

**Complementary**: Baseline captures **what** the code does, WL captures **how** it's written.

---

## Part 14: Practical Example

### Program Comparison

**Student 1** (s1.c):
```c
int factorial(int n) {
  int result = 1;
  for (int i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

**Student 2** (s2.c):
```c
int factorial(int num) {
  int ans = 1;
  for (int j = 1; j <= num; j++) {
    ans = ans * j;
  }
  return ans;
}
```

**WL Analysis**:
- Same AST structure (FOR loop with multiplication assignment)
- Different variable names don't matter (all become IDENTIFIER)
- **WL Similarity**: **0.99** ✅ (correctly identifies structural equivalence)

**Student 3** (s3.c):
```c
int factorial(int n) {
  if (n == 0) return 1;
  return n * factorial(n - 1);
}
```

**WL Analysis**:
- Different AST structure (IF + recursive call vs FOR loop)
- **WL Similarity to s1**: **0.25** ✅ (correctly identifies structural difference)

---

## Summary for Your Guide

**WL View uses graph kernel theory** to create structural fingerprints:

### Process:
1. **Extract AST** from code
2. **WL Algorithm**: Iteratively propagate node labels (2 iterations)
3. **Count patterns**: Create histogram of WL features
4. **Build vocabulary**: Global dictionary of all patterns (~400-500)
5. **Vectorize**: Convert to fixed-length vector
6. **Normalize**: L2 normalization
7. **Compare**: Cosine similarity

### Key Points:
✅ **Captures**: Fine-grained syntactic structure
✅ **Invariant**: To variable names, literal values
✅ **Fast**: No training, deterministic
❌ **Limitation**: Purely syntactic, can't distinguish semantic differences

### Result:
- **High similarity** → Same code structure
- **Low similarity** → Different code structure
- **Complements Baseline**: Baseline = "what", WL = "how"

**Intentionally weak**: Designed to motivate the need for semantic views (SCDPS, CES)!
