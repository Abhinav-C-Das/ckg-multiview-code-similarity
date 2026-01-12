# SCDPS View - Complete Explanation
## (Structural Context-Dependent Path Sequences)

## Overview
The **SCDPS (Structural Context-Dependent Path Sequences) View** is the third view in our multi-view framework. It captures **data and control flow patterns** by tracing paths through the **Program Dependence Graph (PDG)**.

**Key Idea**: Programs with similar data/control relationships exhibit similar path patterns through their PDG, even if their AST structures differ slightly.

---

## Part 1: What is SCDPS?

### The Big Picture
SCDPS extracts **sequences of dependencies** from the PDG:
- **Data dependencies**: "Variable X flows to Y"
- **Control dependencies**: "Statement A controls whether B executes"

**Example**:
```c
int x = 5;           // Node A
if (x > 0) {         // Node B (control dependence from A)
  int y = x + 2;     // Node C (data dependence from A, control from B)
}
```

**SCDPS Path**: `IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-IDENTIFIER`

---

## Part 2: PDG (Program Dependence Graph) Basics

### What is a PDG?
A **Program Dependence Graph** combines:
1. **Data Dependence Graph (DDG)**: Shows data flow
2. **Control Dependence Graph (CDG)**: Shows control flow

### Data Dependence
**Definition**: A data dependence exists from statement S1 to S2 if:
- S1 defines (writes) a variable X
- S2 uses (reads) variable X
- There's a path from S1 to S2 where X is not redefined

**Example**:
```c
int sum = 0;        // S1: defines 'sum'
sum = sum + 10;     // S2: uses 'sum' → DATA DEPENDENCE from S1
```

### Control Dependence
**Definition**: Statement S2 is control-dependent on S1 if:
- S1 is a conditional/loop
- The execution of S2 depends on S1's outcome

**Example**:
```c
if (x > 0) {        // S1: condition
  y = x + 5;        // S2: CONTROL DEPENDENT on S1
}
```

---

## Part 3: SCDPS Algorithm (Step-by-Step)

### Parameters (Fixed):
- **MAX_DEPTH**: 2 (path length limit)
- **MAX_PATHS_PER_START**: 1000 (prevents explosion)

### Allowed Node Types:
```
IDENTIFIER          → Variable usage
CALL                → Function/operator calls
LITERAL             → Constants (5, "hello")
METHOD_PARAMETER_IN → Function parameters
RETURN              → Return statements
```

### Algorithm:

#### Step 1: Select Start Nodes
From each method, collect:
- **METHOD_PARAMETER_IN**: Function parameters
- **IDENTIFIER**: Variable references
- **CALL**: Function calls

#### Step 2: DFS (Depth-First Search)
For each start node, explore outgoing edges:
1. **Data dependence edges** (`_reachingDefOut`)
2. **Control dependence edges** (`_cdgOut`)

Track the **path signature** as you go.

#### Step 3: Build Path Signatures
**Format**: `START-EDGE_TYPE-NODE-EDGE_TYPE-NODE-...`

**Example**:
- Start: `IDENTIFIER` (variable 'sum')
- Follow data edge → `CALL` (operator +=)
- Follow control edge → `IDENTIFIER` (loop counter)

**Path**: `IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-IDENTIFIER`

#### Step 4: Count Occurrences
Create a histogram of all path signatures found.

---

## Part 4: Detailed Example

### Sample Code:
```c
int sum(int arr[], int n) {
  int total = 0;           // Line 2
  for (int i = 0; i < n; i++) {  // Line 3
    total += arr[i];       // Line 4
  }
  return total;            // Line 6
}
```

### PDG Construction:

**Data Dependencies**:
1. `total` (line 2) → `total` used in += (line 4)
2. `total` (line 4) → `total` in return (line 6)
3. `arr` (parameter) → `arr[i]` (line 4)
4. `i` (line 3) → `i` in condition (line 3)
5. `i` (line 3) → `i` in array access (line 4)

**Control Dependencies**:
1. FOR condition (line 3) → body (line 4)

### Path Extraction (Depth 2):

#### Starting from `total` (IDENTIFIER):
**Path 1**:
- Start: `IDENTIFIER` (total)
- Data edge → `CALL` (operator.assignmentPlus)
- **Signature**: `IDENTIFIER-DATA_DEP-CALL`
- **Count**: +1

**Path 2**:
- Start: `IDENTIFIER` (total)
- Data edge → `CALL` (assignmentPlus)
- Control edge → `IDENTIFIER` (loop variable or controlled statement)
- **Signature**: `IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-IDENTIFIER`
- **Count**: +1

#### Starting from `arr` (METHOD_PARAMETER_IN):
**Path 3**:
- Start: `METHOD_PARAMETER_IN` (arr)
- Data edge → `CALL` (indexAccess)
- **Signature**: `METHOD_PARAMETER_IN-DATA_DEP-CALL`
- **Count**: +1

**Path 4**:
- Start: `METHOD_PARAMETER_IN` (arr)
- Data edge → `CALL` (indexAccess)
- Data edge → `CALL` (assignmentPlus)
- **Signature**: `METHOD_PARAMETER_IN-DATA_DEP-CALL-DATA_DEP-CALL`
- **Count**: +1

### Example Output (`scdps.json`):
```json
{
  "IDENTIFIER-DATA_DEP-CALL": 3,
  "IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-IDENTIFIER": 2,
  "IDENTIFIER-DATA_DEP-RETURN": 1,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL": 2,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL-DATA_DEP-CALL": 1,
  "CALL-DATA_DEP-CALL": 4,
  "CALL-CONTROL_DEP-CALL": 2
}
```

---

## Part 5: What SCDPS Captures

### Patterns Detected:

#### 1. **Accumulation Patterns**
```c
sum = 0;
for (...) {
  sum += arr[i];
}
```
**SCDPS sees**:
- `IDENTIFIER-DATA_DEP-CALL` (sum flows to +=)
- `CALL-CONTROL_DEP-IDENTIFIER` (assignment controlled by loop)

#### 2. **Parameter Flow to Return**
```c
int func(int x) {
  return x * 2;
}
```
**SCDPS sees**:
- `METHOD_PARAMETER_IN-DATA_DEP-CALL-DATA_DEP-RETURN`

#### 3. **Conditional Updates**
```c
if (x > max) {
  max = x;
}
```
**SCDPS sees**:
- `IDENTIFIER-CONTROL_DEP-CALL` (assignment under condition)

#### 4. **Array Access in Loops**
```c
for (int i = 0; i < n; i++) {
  arr[i] = ...;
}
```
**SCDPS sees**:
- `IDENTIFIER-DATA_DEP-CALL` (i flows to indexAccess)
- `CALL-CONTROL_DEP-CALL` (indexAccess controlled by loop)

---

## Part 6: SCDPS vs Other Views

### Comparison:

| Feature | Baseline | WL | SCDPS |
|---------|----------|-----|-------|
| **Focus** | Counts | AST structure | Data/Control flow |
| **Graph** | AST + CFG | AST | PDG |
| **Captures** | What & how many | Tree patterns | Dependencies |
| **Semantic?** | Partial (def-use counts) | No | Yes (flow patterns) |
| **Distinguishes** | Recursion vs iteration | Syntax differences | Flow differences |

### What SCDPS Adds:

✅ **Data flow awareness**: Tracks variable propagation
✅ **Control flow context**: Understands conditional execution
✅ **Semantic patterns**: Accumulation, filtering, max-finding
✅ **Deeper than WL**: Goes beyond syntax to dependencies

### SCDPS Limitations:

❌ **Still structural**: Based on code structure, not runtime behavior
❌ **Path explosion**: Can generate many similar paths
❌ **Limited depth**: Only 2 hops (performance constraint)
❌ **Cannot distinguish**: Accumulation vs recomputation (same flow!)

---

## Part 7: Feature Extraction Pipeline

### Step 1: SCDPS Extraction (`scdps_extract.sc`)

**Process**:
```scala
// 1. Load CPG
importCpg("cpg.bin")

// 2. For each method (excluding main):
for (method <- methods) {
  
  // 3. Get PDG nodes (data + control dependencies)
  val pdgNodes = method._reachingDefOut ++ method._cdgOut
  
  // 4. Filter valid start nodes
  val startNodes = pdgNodes.filter(isValidStart)
  
  // 5. DFS from each start node
  for (node <- startNodes) {
    dfs(
      current = node,
      depth = 0,
      path = List(node.label),
      visited = Set(node.id),
      lastEdgeWasControl = false
    )
  }
}

// 6. Output path histogram
println(pathCounts.toJson)
```

**DFS Logic**:
```scala
def dfs(current, depth, path, visited, lastEdgeWasControl) {
  if (depth == MAX_DEPTH) return
  
  // Follow data dependencies
  for (next <- current._reachingDefOut) {
    newPath = path + ["DATA_DEP", next.label]
    count(newPath.signature)
    dfs(next, depth+1, newPath, visited + next, false)
  }
  
  // Follow control dependencies (max one in sequence)
  if (!lastEdgeWasControl) {
    for (next <- current._cdgOut) {
      newPath = path + ["CONTROL_DEP", next.label]
      count(newPath.signature)
      dfs(next, depth+1, newPath, visited + next, true)
    }
  }
}
```

**Output** (`scdps.json`):
```json
{
  "IDENTIFIER-DATA_DEP-CALL": 5,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL": 3,
  "CALL-DATA_DEP-CALL-DATA_DEP-RETURN": 2,
  ...
}
```

---

## Part 8: Vocabulary Building

### Step 2: Build Global Vocabulary (`build_scdps_vocab.py`)

**Same process as WL**:
1. Scan all `scdps.json` files
2. Collect unique path signatures
3. Assign integer IDs
4. Save as `scdps_vocab.json`

**Example Vocabulary**:
```json
{
  "IDENTIFIER-DATA_DEP-CALL": 0,
  "IDENTIFIER-DATA_DEP-RETURN": 1,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL": 2,
  "CALL-DATA_DEP-CALL": 3,
  "IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-IDENTIFIER": 4,
  ...
}
```

**Vocabulary Size**: Typically **200-400** unique path signatures.

(Smaller than WL because paths are more constrained)

---

## Part 9: Vectorization

### Step 3: Convert to Vectors (`vectorize_scdps.py`)

**Same as WL**:
1. Create zero vector of size = vocabulary size
2. For each path in program's `scdps.json`:
   - Find index in vocabulary
   - Set vector[index] = count

**Example**:

**Program's paths**:
```json
{
  "IDENTIFIER-DATA_DEP-CALL": 5,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL": 3,
  "CALL-DATA_DEP-CALL": 4
}
```

**Vocabulary** (size 6):
```json
{
  "IDENTIFIER-DATA_DEP-CALL": 0,
  "IDENTIFIER-DATA_DEP-RETURN": 1,
  "METHOD_PARAMETER_IN-DATA_DEP-CALL": 2,
  "CALL-DATA_DEP-CALL": 3,
  ...
}
```

**Vector**:
```
[5, 0, 3, 4, 0, 0]
 ^  ^  ^  ^  ^  ^
 |  |  |  |  └─ path_5: 0
 |  |  |  └─ path_3 (CALL-DATA_DEP-CALL): 4
 |  |  └─ path_2 (METHOD_PARAMETER_IN-DATA_DEP-CALL): 3
 |  └─ path_1: 0
 └─ path_0 (IDENTIFIER-DATA_DEP-CALL): 5
```

**Output**: `p1_s_s1.vec`

---

## Part 10: Normalization & Similarity

### Step 4: L2 Normalization (`normalize_scdps.py`)

**Same as other views**: Scale to unit length.

```
norm = sqrt(5² + 0² + 3² + 4² + 0² + 0²) = sqrt(50) = 7.07
normalized = [0.707, 0, 0.424, 0.566, 0, 0]
```

### Step 5: Cosine Similarity (`scdps_similarity.py`)

**Same as WL**: Dot product of normalized vectors.

**Example**:

**Student**: `[0.707, 0, 0.424, 0.566, 0, 0]`
**Reference**: `[0.700, 0, 0.420, 0.570, 0, 0]`

**Similarity**:
```
0.707×0.700 + 0×0 + 0.424×0.420 + 0.566×0.570 + ...
= 0.495 + 0 + 0.178 + 0.323
= 0.996
```

**Result**: **0.996** (99.6% similar)

---

## Part 11: Complete Pipeline Flow

```
┌─────────────┐
│  C Program  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Joern (CPG)     │  ← Build PDG
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ scdps_extract.sc │  ← DFS through PDG (depth 2)
└──────┬───────────┘
       │  Extract path signatures
       ▼  scdps.json (per program)
       │
       ├─ All programs →┌───────────────────┐
       │                │build_scdps_vocab.py│  ← Build global vocab
       │                └─────────┬──────────┘
       │                          │
       │                          ▼  scdps_vocab.json (~200-400 paths)
       ├──────────────────────────┘
       │
       ▼
┌──────────────────┐
│vectorize_scdps.py│  ← Convert to vectors
└──────┬───────────┘
       │
       ▼  program.vec
┌──────────────────┐
│normalize_scdps.py│  ← L2 normalization
└──────┬───────────┘
       │
       ▼  program.norm.vec
┌──────────────────┐
│scdps_similarity  │  ← Cosine similarity
└──────┬───────────┘
       │
       ▼
  SCDPS Similarity (0-1)
```

---

## Part 12: Real-World Example

### Program 1: Array Sum (Accumulation)
```c
int sum(int arr[], int n) {
  int total = 0;
  for (int i = 0; i < n; i++) {
    total += arr[i];
  }
  return total;
}
```

**SCDPS Paths**:
- `IDENTIFIER-DATA_DEP-CALL`: 4 (total flows to +=, i flows to <, etc.)
- `METHOD_PARAMETER_IN-DATA_DEP-CALL`: 2 (arr, n flow to operations)
- `CALL-CONTROL_DEP-CALL`: 3 (operations controlled by loop)
- `IDENTIFIER-DATA_DEP-RETURN`: 1 (total flows to return)

### Program 2: Array Sum (Different Variables)
```c
int sum(int numbers[], int size) {
  int result = 0;
  for (int j = 0; j < size; j++) {
    result += numbers[j];
  }
  return result;
}
```

**SCDPS Paths**: **IDENTICAL COUNTS** ✅
- Same flow patterns despite different names

**SCDPS Similarity**: **0.99+** (correctly identifies as same algorithm)

### Program 3: Array Max (Different Flow)
```c
int findMax(int arr[], int n) {
  int max = arr[0];
  for (int i = 1; i < n; i++) {
    if (arr[i] > max) {
      max = arr[i];
    }
  }
  return max;
}
```

**SCDPS Paths**: **DIFFERENT**
- More `CONTROL_DEP` paths (due to if statement)
- Different `IDENTIFIER-DATA_DEP` patterns (max updated conditionally)

**SCDPS Similarity to sum**: **0.65** (correctly identifies different pattern)

---

## Part 13: SCDPS Strengths & Weaknesses

### ✅ Strengths:

1. **Flow-aware**: Captures data and control dependencies
2. **Beyond syntax**: More semantic than WL
3. **Context-sensitive**: Paths include both data and control context
4. **Robust to renaming**: Variable names don't matter

### ❌ Weaknesses:

1. **Still structural**: Based on code structure, not semantics
2. **Cannot distinguish**:
   - Accumulation vs recomputation (same flow graph!)
   - `sum += x` vs `sum = sum + x` (same PDG)
3. **Path explosion**: Many similar paths
4. **Shallow**: Depth 2 limit (performance constraint)

### The Key Limitation:

**Example** (SCDPS cannot distinguish):
```c
// Accumulation
for (int i = 0; i < n; i++) {
  sum += arr[i];    // Accumulate
}

// Recomputation
for (int i = 0; i < n; i++) {
  sum = 0;          // Reset each time!
  sum = arr[i];     // Recompute
}
```

**Both have**:
- `IDENTIFIER-DATA_DEP-CALL` (sum flows to assignment)
- `CALL-CONTROL_DEP-CALL` (controlled by loop)

**SCDPS sees them as SIMILAR** ❌

**This motivates CES!** (the next view)

---

## Part 14: Design Philosophy

### Why Include SCDPS?

1. **Bridges gap**: Between syntax (WL) and semantics (CES)
2. **Flow patterns**: Captures important data/control relationships
3. **Proven technique**: PDG-based similarity is well-established
4. **Complementary**: Adds dimension that others miss

### In the Multi-View Framework:

- **Baseline**: What code does (counts, metrics)
- **WL**: How code is written (AST structure)
- **SCDPS**: How data/control flows ← **Structural flow**
- **CES**: What values do over time ← **Semantic evolution**

---

## Summary for Your Guide

**SCDPS extracts path signatures** through the Program Dependence Graph:

### Algorithm:
1. **Build PDG** from CPG (data + control dependencies)
2. **DFS traversal**: Start from parameters/identifiers
3. **Track paths**: Record sequences like `IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-RETURN`
4. **Count patterns**: Create histogram of path signatures
5. **Vectorize**: Convert to fixed-length vectors (~200-400 dimensions)
6. **Normalize & Compare**: L2 normalization + cosine similarity

### Key Points:
✅ **Captures**: Data flow (def-use) + control flow (conditions)
✅ **Depth 2**: Explores 2-hop neighborhoods in PDG
✅ **Context-aware**: Paths include edge types (DATA vs CONTROL)
❌ **Limitation**: Still structural, can't distinguish semantic differences

### Result:
- **High similarity** → Similar data/control flow patterns
- **Low similarity** → Different dependency structures
- **Complements**: Baseline (metrics), WL (syntax), but **still needs CES for semantics**!

### Example Path:
```
sum          →  DATA_DEP  →  operator+=  →  CONTROL_DEP  →  for_loop
(IDENTIFIER)                 (CALL)                          (CALL)
```
**Signature**: `IDENTIFIER-DATA_DEP-CALL-CONTROL_DEP-CALL`
