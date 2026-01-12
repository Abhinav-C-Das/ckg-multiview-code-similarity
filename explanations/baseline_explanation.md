# Baseline View - Complete Explanation

## Overview
The **Baseline View** is the first view in our multi-view code similarity framework. It extracts **fundamental numeric features** from C programs using static analysis on the Code Property Graph (CPG) built by Joern.

The baseline view combines **3 types of features**:
1. **Structural Features** (9 features) - Program structure and syntax
2. **Semantic Features** (6 features) - Data flow and dependencies
3. **Behavioral Features** (3 features) - Computational patterns

Total: **18 core features** + additional variable role features

---

## Part 1: Feature Extraction (Using Joern Scripts)

### 1.1 STRUCTURAL FEATURES (`basic_structural.sc`)

These features capture **how the program is organized** structurally.

#### **Feature 1: `ast_node_count`**
- **What it is**: Total number of nodes in the Abstract Syntax Tree (AST)
- **What it measures**: Program size/complexity
- **Example**: 
  ```c
  int sum(int a[], int size) {
    int total = 0;
    for (int j = 0; j < size; j++) {
      total += a[j];
    }
    return total;
  }
  ```
  - AST nodes include: function declaration, parameters (a, size), local variable (total), for loop, loop condition, assignment, array access, return statement
  - **Value**: ~45-50 nodes (includes all tokens, operators, identifiers)

#### **Feature 2: `max_ast_depth`**
- **What it is**: Maximum depth of the AST tree
- **What it measures**: Maximum nesting level
- **Example**: In the above code:
  ```
  Function (depth 0)
    └─ Body (depth 1)
         ├─ Variable Declaration (depth 2)
         │    └─ Initializer: 0 (depth 3)
         └─ For Loop (depth 2)
              └─ Loop Body (depth 3)
                   └─ Assignment (depth 4)
                        └─ Array Access (depth 5)
  ```
  - **Value**: 5 or 6 (depending on AST representation)

#### **Feature 3: `avg_ast_depth`**
- **What it is**: Average depth of all AST nodes
- **What it measures**: Overall nesting complexity
- **Example**: For our sum function
  - **Value**: ~3.2 (average across all nodes)

#### **Feature 4: `ast_type_histogram`** (not directly used as single value)
- **What it is**: Count of each type of AST node (IDENTIFIER, CALL, LITERAL, etc.)
- **What it measures**: Distribution of syntactic elements
- **Example**: 
  ```json
  {
    "IDENTIFIER": 12,
    "CALL": 3,
    "LITERAL": 2,
    "CONTROL_STRUCTURE": 1,
    "LOCAL": 1
  }
  ```

#### **Feature 5: `cfg_node_count`**
- **What it is**: Number of nodes in the Control Flow Graph (CFG)
- **What it measures**: Number of execution points
- **Example**: 
  ```c
  int total = 0;        // Node 1
  for (int j = 0;       // Node 2 (init)
       j < size;        // Node 3 (condition)
       j++) {           // Node 4 (increment)
    total += a[j];      // Node 5 (body)
  }
  return total;         // Node 6
  ```
  - **Value**: ~6-8 nodes

#### **Feature 6: `cfg_edge_count`**
- **What it is**: Number of edges (transitions) in the CFG
- **What it measures**: Control flow complexity
- **Example**: 
  ```
  Node 1 → Node 2 → Node 3 → Node 5 → Node 4 → Node 3 (loop back)
  Node 3 → Node 6 (exit condition)
  ```
  - **Value**: ~7-9 edges

#### **Feature 7: `conditional_count`**
- **What it is**: Number of IF and SWITCH statements
- **What it measures**: Branching complexity
- **Example**:
  ```c
  if (x > 0) {      // conditional_count = 1
    if (x < 10) {   // conditional_count = 2
      // ...
    }
  }
  ```

#### **Feature 8: `loop_count`**
- **What it is**: Number of loops (FOR, WHILE, DO, FOREACH)
- **What it measures**: Iterative complexity
- **Example**:
  ```c
  for (int i = 0; i < n; i++) {     // loop_count = 1
    for (int j = 0; j < m; j++) {   // loop_count = 2
      // nested loops
    }
  }
  ```

#### **Feature 9: `ternary_count`**
- **What it is**: Number of ternary operators (? :)
- **What it measures**: Inline conditional expressions
- **Example**:
  ```c
  int max = (a > b) ? a : b;  // ternary_count = 1
  ```

---

### 1.2 SEMANTIC FEATURES (`basic_semantic.sc`)

These features capture **how data flows** through the program.

#### **Feature 10: `def_use_edges`**
- **What it is**: Number of definition-use relationships (where a variable is defined and where it's used)
- **What it measures**: Data dependency complexity
- **How it's extracted**: Uses symbol resolution in AST (NOT full dataflow - to avoid Joern hangs)
- **Example**:
  ```c
  int total = 0;        // Definition of 'total'
  for (int j = 0; j < size; j++) {
    total += a[j];      // Use of 'total' (def-use edge 1)
  }
  return total;         // Use of 'total' (def-use edge 2)
  ```
  - **Value**: 2 (total has 2 uses)
  - Similarly, `j` has def-use edges for condition and increment
  - **Total def_use_edges**: ~5-8

#### **Feature 11: `def_use_density`**
- **What it is**: Ratio of def-use edges to total variable uses
- **What it measures**: How tightly variables are connected
- **Formula**: `def_use_edges / total_variable_uses`
- **Example**: If we have 10 variable uses and 7 def-use edges
  - **Value**: 0.7

#### **Feature 12: `control_predicates`**
- **What it is**: Total number of control structures (IF, SWITCH, FOR, WHILE, DO)
- **What it measures**: Control flow complexity
- **Example**:
  ```c
  for (int i = 0; i < n; i++) {    // control_predicate 1
    if (arr[i] > max) {             // control_predicate 2
      max = arr[i];
    }
  }
  ```
  - **Value**: 2

#### **Feature 13: `control_data_ratio`**
- **What it is**: Ratio of control predicates to def-use edges
- **What it measures**: Balance between control flow and data flow
- **Formula**: `control_predicates / def_use_edges`
- **Example**: 2 control predicates, 8 def-use edges
  - **Value**: 0.25 (more data-driven than control-driven)

#### **Feature 14: `param_return_ratio`**
- **What it is**: Ratio of parameters used in return statements
- **What it measures**: Input-output dependency
- **Example**:
  ```c
  int add(int a, int b) {
    return a + b;  // Both 'a' and 'b' used in return
  }
  ```
  - **Value**: 1.0 (2/2 parameters used in return)
  
  ```c
  int process(int x, int y) {
    int result = x * 2;
    return result;  // Only 'x' used (indirectly), 'y' not used
  }
  ```
  - **Value**: 0.5 (1/2 parameters used)

#### **Feature 15: `param_output_ratio`**
- **What it is**: Ratio of parameters used in output statements (printf, puts)
- **What it measures**: Parameter usage in I/O
- **Example**:
  ```c
  void display(int x, int y) {
    printf("%d\n", x);  // Only 'x' used in output
  }
  ```
  - **Value**: 0.5 (1/2 parameters used in output)

---

### 1.3 BEHAVIORAL FEATURES (`basic_behavioral.sc`)

These are **binary flags** indicating computational patterns.

#### **Feature 16: `recursion_present`**
- **What it is**: 1 if function calls itself, 0 otherwise
- **What it measures**: Recursive approach
- **Example**:
  ```c
  int factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);  // Calls itself
  }
  ```
  - **Value**: 1

#### **Feature 17: `iterative_present`**
- **What it is**: 1 if any loop exists, 0 otherwise
- **What it measures**: Iterative approach
- **Example**:
  ```c
  int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {  // Loop exists
      result *= i;
    }
    return result;
  }
  ```
  - **Value**: 1

#### **Feature 18: `base_case_present`**
- **What it is**: 1 if recursion has a base case (IF with return), 0 otherwise
- **What it measures**: Proper recursive structure
- **Example**:
  ```c
  int factorial(int n) {
    if (n == 0) return 1;  // Base case with return inside IF
    return n * factorial(n - 1);
  }
  ```
  - **Value**: 1 (only if recursion_present = 1)

---

## Part 2: Complete Example with Real Values

Let's trace through our sample program:

```c
#include <stdio.h>

int sum(int a[], int size) {
  int total = 0;
  for (int j = 0; j < size; j++) {
    total += a[j];
  }
  return total;
}

int main() {
  int numbers[] = {5, 10, 15, 20, 25};
  printf("Sum = %d\n", sum(numbers, 5));
  return 0;
}
```

### Extracted Features (JSON):
```json
{
  "ast_node_count": 87,
  "max_ast_depth": 6,
  "avg_ast_depth": 3.5,
  "cfg_node_count": 15,
  "cfg_edge_count": 18,
  "conditional_count": 0,
  "loop_count": 1,
  "ternary_count": 0,
  
  "def_use_edges": 12,
  "def_use_density": 0.75,
  "control_predicates": 1,
  "control_data_ratio": 0.083,
  "param_return_ratio": 0.5,
  "param_output_ratio": 0.0,
  
  "recursion_present": 0,
  "iterative_present": 1,
  "base_case_present": 0
}
```

---

## Part 3: Vectorization Pipeline

### Step 1: Feature Aggregation
**Script**: `similarity/aggregate_baseline.py`

This script combines all three JSON files:
- `structural.json`
- `semantic.json`
- `behavioral.json`
- `variable_roles.json` (if present)

**Output**: `combined_features.json` containing all features in one file

### Step 2: Vectorization
**Script**: `similarity/vectorize_features.py`

**What it does**: Converts the JSON features into a **fixed-length numeric vector**

**Feature Order** (CRITICAL - must be consistent):
```python
FEATURE_ORDER = [
    # Structural (indices 0-7)
    "ast_node_count",      # index 0
    "max_ast_depth",       # index 1
    "avg_ast_depth",       # index 2
    "cfg_node_count",      # index 3
    "cfg_edge_count",      # index 4
    "conditional_count",   # index 5
    "loop_count",          # index 6
    "ternary_count",       # index 7
    
    # Semantic (indices 8-13)
    "def_use_edges",       # index 8
    "def_use_density",     # index 9
    "control_predicates",  # index 10
    "control_data_ratio",  # index 11
    "param_return_ratio",  # index 12
    "param_output_ratio",  # index 13
    
    # Behavioral (indices 14-16)
    "recursion_present",   # index 14
    "iterative_present",   # index 15
    "base_case_present",   # index 16
    
    # Additional features (if present)
    # ... variable role features
]
```

**Example Vector** (for our sum program):
```
87, 6, 3.5, 15, 18, 0, 1, 0, 12, 0.75, 1, 0.083, 0.5, 0.0, 0, 1, 0
```

**Output File**: `p1_s_s1.vec` (comma-separated values)

---

## Part 4: Normalization

### L2 Normalization
**Script**: `similarity/normalize.py`

**What it does**: Normalizes the vector to unit length (magnitude = 1)

**Why?** To make vectors comparable regardless of program size

**Formula**:
```
normalized_vector[i] = vector[i] / ||vector||
where ||vector|| = sqrt(sum(x² for x in vector))
```

**Example**:
Original vector: `[87, 6, 3.5, 15, 18, 0, 1, 0, 12, 0.75, 1, 0.083, 0.5, 0, 0, 1, 0]`

L2 Norm: `sqrt(87² + 6² + 3.5² + 15² + ... + 0²) = 91.23`

Normalized: `[0.953, 0.066, 0.038, 0.164, 0.197, 0, 0.011, 0, 0.131, 0.008, 0.011, 0.001, 0.005, 0, 0, 0.011, 0]`

**Output File**: `p1_s_s1.norm.vec`

---

## Part 5: Similarity Calculation

### Cosine Similarity
**Script**: `similarity/similarity.py`

**What it does**: Compares two normalized vectors using **cosine similarity**

**Formula**:
```
cosine_similarity = (A · B) / (||A|| × ||B||)

For normalized vectors (||A|| = ||B|| = 1):
cosine_similarity = A · B  (dot product)
```

**How it works**:
1. Load two normalized vectors (student and reference)
2. Compute similarity for each feature group:
   - **Structural similarity**: cosine of indices 0-7
   - **Semantic similarity**: cosine of indices 8-13
   - **Behavioral similarity**: cosine of indices 14-16
3. Compute **overall similarity**: average of three similarities

**Example**:

Student vector (s1): `[0.953, 0.066, 0.038, ..., 0.011, 0]`
Reference vector (ref1): `[0.948, 0.070, 0.041, ..., 0.010, 0]`

**Structural Similarity**:
```
A_struct = [0.953, 0.066, 0.038, 0.164, 0.197, 0, 0.011, 0]
B_struct = [0.948, 0.070, 0.041, 0.160, 0.195, 0, 0.012, 0]

dot(A_struct, B_struct) = 0.953×0.948 + 0.066×0.070 + ... = 0.96
```

**Semantic Similarity**: 0.94
**Behavioral Similarity**: 1.0 (both are iterative, non-recursive)

**Overall Similarity**: `(0.96 + 0.94 + 1.0) / 3 = 0.967` ✅ **96.7% similar**

**Output** (JSON):
```json
{
  "structural_similarity": 0.96,
  "semantic_similarity": 0.94,
  "behavioral_similarity": 1.0,
  "overall_similarity": 0.967
}
```

---

## Part 6: Key Design Decisions

### Why No Full Dataflow?
- Joern's `runDataflow()` can **hang** or cause **memory issues** on large programs
- We use **local, intra-procedural** def-use analysis instead
- This is **conservative** but **stable** and **fast**
- **Research-defensible**: Standard practice in code similarity literature

### Why This Specific Feature Set?
- **Structural**: Captures syntax and organization
- **Semantic**: Captures data dependencies and flow
- **Behavioral**: Captures high-level computational patterns
- **Complementary**: Together they provide multi-faceted view of code

### Why Separate Similarity Scores?
- Allows **interpretability**: "Programs are structurally similar but semantically different"
- Enables **weighted fusion**: Can adjust weights later
- Provides **diagnostic information**: Helps understand why programs are/aren't similar

---

## Part 7: Complete Pipeline Flow

```
┌─────────────┐
│  C Program  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Joern (CPG)    │  ← Generate Code Property Graph
└──────┬──────────┘
       │
       ├─→ basic_structural.sc  → structural.json
       ├─→ basic_semantic.sc    → semantic.json
       └─→ basic_behavioral.sc  → behavioral.json
       │
       ▼
┌──────────────────────┐
│ aggregate_baseline.py│  ← Combine all features
└──────┬───────────────┘
       │
       ▼  combined_features.json
┌──────────────────────┐
│ vectorize_features.py│  ← Convert to vector
└──────┬───────────────┘
       │
       ▼  program.vec
┌──────────────────────┐
│    normalize.py      │  ← L2 normalization
└──────┬───────────────┘
       │
       ▼  program.norm.vec
┌──────────────────────┐
│   similarity.py      │  ← Compare with reference
└──────┬───────────────┘
       │
       ▼
   Similarity Score (0-1)
```

---

## Summary for Your Guide

**Baseline View extracts 18 numeric features** from C programs:
- **9 Structural** (AST/CFG metrics)
- **6 Semantic** (def-use, control-data relationships)
- **3 Behavioral** (recursion, iteration flags)

**Processing**: JSON → Vector → Normalized Vector → Cosine Similarity

**Result**: Similarity scores (0-1) for structural, semantic, behavioral, and overall similarity

**Strength**: Fast, stable, interpretable, research-proven
**Limitation**: Cannot distinguish semantically different programs with identical structure (motivates other views)
