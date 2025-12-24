#!/usr/bin/env bash
set -e

echo "========================================"
echo "[FULL PIPELINE] Starting full pipeline"
echo "========================================"

# --------------------------------------------------
# 0. CPG + feature extraction (per-program reuse)
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 0: Running Joern / CPG feature extraction"
./experiments/run_joern.sh

# --------------------------------------------------
# 1. Baseline pipeline
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 1: Running BASELINE pipeline"
./experiments/pipeline/run_baseline_pipeline.sh

# --------------------------------------------------
# 2. WL pipeline
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 2: Running WL pipeline"
./experiments/pipeline/run_wl_pipeline.sh

# --------------------------------------------------
# 3. SCDPS pipeline
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 3: Running SCDPS pipeline"
./experiments/pipeline/run_scdps_pipeline.sh

# --------------------------------------------------
# 4. CES pipeline (NEW)
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 4: Running CES pipeline"
./experiments/pipeline/run_ces_pipeline.sh

# --------------------------------------------------
# 5. Aggregate baseline + WL + SCDPS + CES
# --------------------------------------------------
echo
echo "[FULL PIPELINE] Step 5: Aggregating all features"
python3 evaluation/aggregate_all_features_with_ces.py

echo
echo "[FULL PIPELINE] ✅ Full pipeline completed"
