# Multi-View Code Similarity for Pedagogical Assessment

## Problem Statement

When students submit code for the same programming problem, identifying which reference solution their approach matches is challenging. Traditional similarity metrics fail to distinguish between programs with identical control structures but fundamentally different computational strategies. For example:

```c
// Accumulation approach
int sum(int arr[], int n) {
  int total = 0;
  for (int i = 0; i < n; i++) {
    total += arr[i];
  }
  return total;
}

// Recomputation approach (incorrect)
int sum(int arr[], int n) {
  int result;
  for (int i = 0; i < n; i++) {
    result = arr[i];
  }
  return result;
}
```

These programs have nearly identical AST structure, control flow, and data dependencies, yet represent completely different computational approaches. The accumulation version correctly sums array elements, while the recomputation version only returns the last element.

## System Architecture

The system employs a multi-view framework combining four complementary code representations. Each view captures different aspects of program semantics, and their fusion achieves robust similarity assessment.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Student Code (C)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Joern 4.x     │
                    │  CPG Generator │
                    └────────┬───────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼──────┐          ┌──────▼───────┐
        │ Canonicalize │          │  Build CPG   │
        │  Variables   │          │  (AST, CFG,  │
        │              │          │   PDG, DFG)  │
        └───────┬──────┘          └──────┬───────┘
                │                        │
                └───────────┬────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐      ┌───────▼───────┐      ┌───▼────┐
    │Baseline│      │      WL       │      │ SCDPS  │
    │Features│      │  (Graph       │      │ (PDG   │
    │        │      │   Kernel)     │      │ Paths) │
    └───┬────┘      └───────┬───────┘      └───┬────┘
        │                   │                  │
        │           ┌───────▼──────┐           │
        │           │     CES      │           │
        │           │ (Evolution   │           │
        │           │  Patterns)   │           │
        │           └───────┬──────┘           │
        │                   │                  │
        └───────────────────┼──────────────────┘
                            │
                    ┌───────▼────────┐
                    │   Vectorize    │
                    │   & Normalize  │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │    Compute     │
                    │  Similarities  │
                    │   (Cosine)     │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │   Multi-View   │
                    │     Fusion     │
                    │  (Averaging)   │
                    └───────┬────────┘
                            │
                            ▼
                   Best Match Reference
```

## View 1: Baseline Features

The baseline view extracts 18 numeric features capturing structural complexity, semantic relationships, and behavioral patterns.

### Feature Categories

**Structural Features (9):**
- ast_node_count: Total AST nodes
- max_ast_depth: Maximum tree depth
- avg_ast_depth: Average node depth
- cfg_node_count: Control flow graph nodes
- cfg_edge_count: Control flow edges
- conditional_count: Number of IF/SWITCH statements
- loop_count: Number of FOR/WHILE/DO loops
- ternary_count: Ternary operator occurrences

**Semantic Features (6):**
- def_use_edges: Definition-use relationships
- def_use_density: Ratio of def-use edges to variable uses
- control_predicates: Total control structures
- control_data_ratio: Control flow vs data flow balance
- param_return_ratio: Parameters used in return statements
- param_output_ratio: Parameters used in output calls

**Behavioral Features (3):**
- recursion_present: Binary flag for recursion
- iterative_present: Binary flag for iteration
- base_case_present: Binary flag for recursive base case

### Processing

Features are extracted via Joern queries on the CPG, aggregated into a JSON object, vectorized into an 18-dimensional vector, and L2-normalized. Similarity uses cosine distance on the normalized vector.

## View 2: Weisfeiler-Lehman Graph Kernel

WL applies iterative label refinement to the AST, creating structural fingerprints invariant to variable naming.

### Algorithm

**Iteration 0:** Initialize labels with AST node types (IDENTIFIER, CALL, LITERAL, etc.)

**Iteration 1:** Each node combines its label with sorted children labels:
```
new_label = hash(current_label + "|" + sorted_children_labels)
```

**Iteration 2:** Repeat with refined labels from iteration 1.

**Output:** Histogram of label counts across all iterations.

### Example

For a FOR loop containing an assignment:
```
Iteration 0: CONTROL_STRUCTURE (count: 1), CALL (count: 2)
Iteration 1: hash("CONTROL_STRUCTURE|BLOCK,CALL,LOCAL") → 7a3f9b...
Iteration 2: hash("7a3f9b...|e4d2c1...,f8b6a3...") → 2c4e7f...
```

Creates approximately 400-500 unique structural patterns per program.

### Processing

Patterns extracted via Scala script, global vocabulary built across all programs, count vectors created (vocabulary size dimensions), L2-normalized, and compared using cosine similarity.

## View 3: SCDPS (Structural Context-Dependent Path Sequences)

SCDPS captures data and control flow patterns by extracting path sequences through the Program Dependence Graph.

### PDG Components

**Data Dependence:** Variable X at statement S1 flows to statement S2 if S1 defines X and S2 uses X.

**Control Dependence:** Statement S2 is control-dependent on S1 if S1 determines whether S2 executes.

### Path Extraction

Starting from parameters and identifiers, depth-first search (depth limit: 2) traverses:
- Data dependence edges (reachingDefOut)
- Control dependence edges (cdgOut)

Recording sequences like:
```
IDENTIFIER → DATA_DEP → CALL → CONTROL_DEP → IDENTIFIER
METHOD_PARAMETER_IN → DATA_DEP → CALL → DATA_DEP → RETURN
```

### Example Paths

For `total += arr[i]` in a loop:
```
total (IDENTIFIER) → DATA_DEP → operator+= (CALL)
arr (METHOD_PARAMETER_IN) → DATA_DEP → indexAccess (CALL)
operator+= (CALL) → CONTROL_DEP → FOR (CONTROL_STRUCTURE)
```

Generates approximately 200-400 unique path signatures per program.

### Processing

Paths extracted via Joern PDG queries, signatures created by concatenating node types and edge types, global vocabulary built, count vectors generated, L2-normalized, and similarity computed via cosine distance.

## View 4: CES (Computation Evolution Signatures)

CES is the novel contribution of this work. It explicitly models how variable values evolve across loop iterations and recursive calls, distinguishing computational strategies that appear identical structurally.

### Evolution Pattern Taxonomy

**Loop Patterns:**

1. ACCUMULATIVE
   - Pattern: `x += val`, `x *= val`, `x = x + val`
   - Semantics: Variable grows/shrinks incrementally
   - Example: `sum += arr[i]`

2. RECOMPUTED
   - Pattern: `x = new_value` (no self-reference)
   - Semantics: Variable replaced each iteration
   - Example: `last = arr[i]`

3. MAX_UPDATE
   - Pattern: `if (val > max) max = val`
   - Semantics: Conditional maximum tracking
   - Detection: Assignment under condition containing ">" and variable name

4. MIN_UPDATE
   - Pattern: `if (val < min) min = val`
   - Semantics: Conditional minimum tracking
   - Detection: Assignment under condition containing "<" and variable name

5. NARROWING_WINDOW
   - Pattern: `left = mid + 1`, `right = mid - 1`
   - Semantics: Binary search bounds shrinking
   - Detection: Canonicalized v0/v1 updated with mid/arithmetic

6. CONTROL_GATED
   - Pattern: Assignment inside IF/SWITCH (not max/min)
   - Semantics: Conditional update
   - Detection: Under control guard without comparison pattern

7. SEARCH_WITH_RETURN
   - Pattern: `if (condition) return value;`
   - Semantics: Early loop exit
   - Detection: Return statement inside conditional within loop

8. COMPARISON_CHAIN
   - Pattern: `arr[i] == arr[n-1-i]`
   - Semantics: Symmetric comparison (palindrome, reversal)
   - Detection: Comparison with forward and backward indexing

9. CONDITIONAL_SWAP
   - Pattern: `if (arr[i] > arr[i+1]) { temp = arr[i]; ... }`
   - Semantics: Sorting swap operation
   - Detection: Temp variable under comparison guard

**Recursive Patterns:**

10. ACCUMULATIVE (Recursive)
    - Pattern: `return n * factorial(n-1)`
    - Semantics: Combines recursive result
    - Detection: Recursive call within arithmetic operation

11. RECOMPUTED (Recursive)
    - Pattern: `return search(arr, target, i+1)`
    - Semantics: Passes through without combination
    - Detection: Recursive call as direct return value

### Detection Algorithm

**Step 1: Variable Canonicalization**

Variables are renamed to canonical form (v0, v1, v2, ...) based on order of appearance. This ensures `sum` and `total` are treated as the same variable role.

**Step 2: Loop Analysis**

For each loop:
- Identify induction variables (loop counters)
- Extract all assignments to non-induction variables
- Classify each assignment's evolution pattern

**Step 3: Pattern Classification**

Decision tree:
```
if accumulative_operator (+=, -=, *=, /=):
    if under_control_guard:
        if condition_contains_greater_than_and_variable:
            → MAX_UPDATE
        elif condition_contains_less_than_and_variable:
            → MIN_UPDATE
        else:
            → CONTROL_GATED
    else:
        → ACCUMULATIVE
elif regular_assignment (=):
    if canonicalized_name in {v0, v1} and rhs_contains_mid:
        → NARROWING_WINDOW
    elif temp_variable_name and under_comparison_guard:
        → CONDITIONAL_SWAP
    elif under_control_guard:
        → CONTROL_GATED
    else:
        → RECOMPUTED
```

**Step 4: Output Generation**

Each detected pattern produces a record:
```json
{
  "context": "loop_FOR",
  "evolution": "ACCUMULATIVE",
  "operator": "ADD"
}
```

### Processing

CES records extracted via custom Joern script, signatures created as `context::evolution::operator`, global vocabulary built (30-60 unique patterns), count vectors generated, L2-normalized, and similarity computed.

### Key Advantage

CES distinguishes the accumulation vs recomputation example:
- Accumulation: `loop_FOR::ACCUMULATIVE::ADD`
- Recomputation: `loop_FOR::RECOMPUTED::ASSIGN`
- Similarity: 0% (correctly identifies different strategies)

## Multi-View Fusion

Similarity scores from all four views are combined using simple averaging:

```
final_similarity = (baseline_sim + wl_sim + scdps_sim + ces_sim) / 4
```

Weighted fusion was explored but equal weights (0.25 each) performed optimally, suggesting each view contributes unique, equally valuable information.

## Dataset

- 15 programming problems covering array operations, search algorithms, recursion, sorting, and string manipulation
- 100 student submissions (6-8 per problem) with varying approaches and styles
- 30 reference solutions (2-3 per problem) representing different valid strategies
- Ground truth annotations based on computational strategy rather than surface syntax

## Experimental Results

### Overall Performance

The multi-view system achieves 89% accuracy (89 out of 100 correct matches).

### Individual View Performance

| View | Accuracy | Features | Dimension |
|------|----------|----------|-----------|
| Baseline | ~75% | 18 metrics | 18 |
| WL | ~88% | AST patterns | 400-500 |
| SCDPS | ~85% | PDG paths | 200-400 |
| CES | ~82% | Evolution patterns | 30-60 |
| Fusion | 89% | Combined | - |

### Baseline Comparison

| Approach | Method | Graph Type | Accuracy | Interpretable |
|----------|--------|------------|----------|---------------|
| CodeBERT | Learned embeddings | None (tokens) | 66% | No |
| GraphCodeBERT | Learned embeddings | Data flow | 88% | No |
| WL (this work) | Explicit analysis | AST | 88% | Partial |
| Multi-view (this work) | Explicit analysis | CPG | 89% | Yes |

### Key Findings

The 22% performance gap between CodeBERT (66%) and GraphCodeBERT (88%) demonstrates that graph structure, particularly data flow information, is essential for code similarity. Pure token-based approaches fail to capture computational semantics.

The multi-view system matches GraphCodeBERT's accuracy (89% vs 88%) while providing interpretable explanations. Unlike learned models which operate as black boxes, the system can identify specific pattern differences (ACCUMULATIVE vs RECOMPUTED) valuable for educational feedback.

### Error Analysis

Analysis of the 11 incorrect predictions reveals:

**Borderline cases (55%):** Similarity scores differ by less than 0.05 between top predictions. These are genuinely ambiguous cases where even GraphCodeBERT produces errors.

**Inherent ambiguity (27%):** Student code legitimately matches multiple references equally well (e.g., simple iteration patterns that could serve multiple purposes).

**Novel patterns (18%):** Students used creative approaches not represented in the CES pattern taxonomy. This indicates areas for pattern expansion rather than fundamental limitations.

**Error concentration:** 73% of errors occur in just 3 out of 15 problems, suggesting problem-specific ambiguity rather than systematic weakness.

## Technical Implementation

### Tools and Libraries

- Joern 4.x for CPG generation and graph queries
- Python 3.8+ for feature processing, vectorization, and similarity computation
- NumPy and SciPy for vector operations and cosine similarity
- JSON for feature storage and interchange

### Performance Characteristics

- CPG generation: 2-3 seconds per program
- Feature extraction: 1-2 seconds per view per program
- Similarity computation: <0.1 seconds for 100 comparisons
- Total pipeline: ~5 minutes for 100 programs

### Design Decisions

**No full dataflow analysis:** Joern's runDataflow() can cause hangs on certain programs. Local, intra-procedural def-use analysis provides sufficient semantic information while maintaining stability.

**Depth limits:** WL uses 2 iterations, SCDPS uses 2-hop paths. Deeper analysis produces exponentially more features without significant accuracy gains.

**Simple fusion:** Equal weighting outperformed optimized weights, suggesting views contribute orthogonal information.

## Contributions

### Novel Aspects

CES (Computation Evolution Signatures) represents the first interpretable semantic abstraction explicitly modeling variable evolution across iterations and recursion. Unlike learned representations, CES patterns are human-understandable and pedagogically meaningful.

The multi-view framework demonstrates that explicit graph analysis can match state-of-the-art learned models without requiring training data or producing black-box predictions.

### Validation

The 22% gap between token-based and graph-based approaches validates the fundamental importance of structural analysis for code similarity.

Error analysis shows that remaining challenges are primarily inherent ambiguities rather than systematic flaws, with both learned and explicit approaches struggling on the same difficult cases.

### Practical Impact

The system enables automatic clustering of student submissions by computational approach, identification of which reference solution each student followed, and generation of specific feedback explaining differences (e.g., "This uses ACCUMULATIVE pattern, reference uses RECOMPUTED").

This interpretability distinguishes the work from learned models and provides direct pedagogical value.

## Limitations and Future Work

### Current Limitations

The CES pattern taxonomy is manually designed and may not cover all possible computational approaches. The system is currently implemented for C/C++ and would require pattern redefinition for other languages. Borderline cases (~5% of dataset) remain genuinely ambiguous even to human annotators.

### Future Directions

Expanding the CES pattern taxonomy based on error analysis and novel student approaches could improve coverage. Per-problem weight optimization with proper cross-validation might capture problem-specific characteristics. Extension to additional programming languages (Python, Java) would demonstrate generalizability. Interactive refinement allowing instructors to define new patterns would enable domain adaptation.

## Conclusion

This work demonstrates that explicit multi-view graph analysis can achieve competitive accuracy (89%) with state-of-the-art learned models (88%) while maintaining interpretability. The novel CES component fills a critical gap in semantic understanding, distinguishing computational strategies that appear structurally identical. The system provides practical value for programming education through its ability to explain similarity decisions using pedagogically meaningful patterns.
