#!/usr/bin/env bash
set -e

for d in data/p*; do
  [ -d "$d" ] || continue
  basename "$d"
done
