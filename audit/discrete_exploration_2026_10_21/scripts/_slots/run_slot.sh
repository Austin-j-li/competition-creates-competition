#!/usr/bin/env bash
# Run one command while it holds one of the team's 8 CPU slots.
# Usage: bash run_slot.sh <command> [args...]
# The call waits until a slot is free. One slot covers one process.
# BLAS thread pools are set to one thread.
SLOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/locks"
mkdir -p "$SLOT_DIR"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
while true; do
  for i in 1 2 3 4 5 6 7 8; do
    exec {fd}>"$SLOT_DIR/slot$i.lock"
    if flock -n "$fd"; then
      echo "[run_slot] slot $i acquired by pid $$: $*" >&2
      "$@"
      status=$?
      flock -u "$fd"
      exec {fd}>&-
      exit $status
    fi
    exec {fd}>&-
  done
  sleep 5
done
