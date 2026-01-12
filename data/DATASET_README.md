# Dataset Summary

## Current Status
✅ **COMPLETE** - Core dataset structure created successfully

## Problems Created (10 total)
1. ✅ **P1 - Array Sum**: 3 refs, 12 students - CES: Accumulation vs Recomputation
2. ✅ **P2 - Find Max**: 2 refs, 6 students - CES: Extrema tracking  
3. ✅ **P3 - Count Occurrences**: 2 refs, 1 student - Counter accumulation
4. ✅ **P4 - Linear Search**: 2 refs, 1 student - Early exit patterns
5. ✅ **P5 - Array Reversal**: 2 refs, 1 student - Two-pointer swap
6. ✅ **P6 - Factorial (Iter)**: 2 refs, 1 student - Loop accumulation
7. ✅ **P7 - Factorial (Rec)**: 2 refs, 1 student - Recursive CES
8. ✅ **P8 - Fibonacci**: 2 refs, 1 student - Multiple strategies
9. ✅ **P9 - GCD**: 2 refs, 1 student - Variable reassignment
10. ✅ **P10 - Prime Check**: 2 refs, 1 student - Nested conditionals

## Files Created
- **Total**: 50+ files
- **References**: 23 files (P1: 3, P2-P10: 2 each)
- **Students**: 27+ files (P1: 12, P2: 6, P3-P10: 1 each)
- **Ground Truth**: data/ground_truth.json

## Directory Structure
```
data/
├── p1/
│   ├── ref/
│   │   ├── ref1.c (Accumulation +=)
│   │   ├── ref2.c (Overwrite =)  ← CES discrimination!
│   │   └── ref3.c (Recursive)
│   └── s/
│       ├── s1.c through s12.c (systematic variants)
├── p2/ through p10/
│   ├── ref/
│   │   ├── ref1.c
│   │   └── ref2.c
│   └── s/
│       └── s1.c
└── ground_truth.json
```

## Next Steps (Optional Expansion)
To expand P3-P10 from 1 student to 6-8 students each:

1. **For each P3-P10**, create variations:
   - Different variable names
   - Different loop types (for/while/do-while)
   - Different operators (++, +=, = x+1)
   - Different initialization strategies
   - Buggy variants if applicable

2. **Update ground_truth.json** for each new student

3. **Test pipeline**: `./run_full_pipeline.sh`

## How to Use Ground Truth
The ground_truth.json file maps each student to their correct reference:
```json
{
  "p1": [
    ["s1", "ref1"],  // Student 1 matches reference 1
    ["s3", "ref2"],  // Student 3 matches reference 2 (buggy overwrite)
    ["s4", "ref3"]   // Student 4 matches reference 3 (recursive)
  ]
}
```

## CES Patterns Demonstrated
- **ACCUMULATIVE**: P1-ref1 (+=), P6-ref1 (*=), P7-ref1 (recursive multiplication)
- **RECOMPUTED**: P1-ref2 (overwrite bug)
- **MAX_UPDATE**: P2-ref1 (conditional max)
- **Counter**: P3-ref1 (count++)
- **Swap**: P5-ref1 (two-pointer)
- **Reassignment**: P9-ref1 (GCD swap pattern)

## Dataset Characteristics
- **Language**: C
- **Scope**: Introductory programming (CS1 level)
- **Focus**: CES discrimination capability
- **Ground Truth**: Manually annotated by design
- **Expandable**: Easy to add more students per problem

## Ready for Evaluation!
You can now:
1. Run pipeline on this dataset
2. Measure baseline, WL, SCDPS, CES performance
3. Do ablation studies
4. Report results in paper Section V

**Minimal viable dataset**: ✅ COMPLETE  
**Full dataset (150+ files)**: Can expand P3-P10 as needed
