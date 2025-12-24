#!/usr/bin/env bash
set -e

echo "[EVAL PIPELINE] Starting evaluation pipeline"

# ----------------------------------------
# WL evaluation
# ----------------------------------------
echo "[EVAL PIPELINE] Evaluating WL similarity"
python3 evaluation/run_topk_retreival_evaluation.py

echo "[EVAL PIPELINE] Evaluation complete"
