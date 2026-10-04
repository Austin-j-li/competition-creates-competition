#!/usr/bin/env bash
# Replay of every numerics step in the order it runs. Each step writes CSV; render.py runs last and only reads.
# Usage: bash run_all.sh [from_step]    (steps are numbered; default 1). Logs: log_<step>.txt, run_all.log.
# thresholds.py writes the oracle and island columns; lp_refine.py and --merge-lp add the exact-LP island threshold.
# About 3 hours on 4 cores.
cd "$(dirname "$0")" || exit 1
from=${1:-1}
n=0
step() {                       # step "name" command...
  n=$((n + 1)); name=$1; shift
  [ "$n" -lt "$from" ] && return 0
  echo "$(date +%H:%M:%S) step $n: $name" >> run_all.log
  "$@" > "log_${name}.txt" 2>&1 || echo "$(date +%H:%M:%S) FAILED: $name" >> run_all.log
}
step weak_r0          python3 weak_r0.py
step sweep_025        python3 run_sweep.py r3 0.25
step verify_025       python3 verify_csv.py eq_r3_rho0.25.csv
step sweep_01         python3 run_sweep.py r3 0.1
step sweep_05         python3 run_sweep.py r3 0.5
step verify_01        python3 verify_csv.py eq_r3_rho0.1.csv --every 5
step verify_05        python3 verify_csv.py eq_r3_rho0.5.csv --every 5
step thresholds       python3 thresholds.py
step region           python3 run_region.py
step verify_region    python3 verify_csv.py eq_region.csv --every 5
step lp_map           python3 lp_map.py r3 0.25
step lp_export        python3 lp_export.py
step verify_lp        python3 verify_csv.py lp_polished.csv
step lp_region        python3 lp_map.py region
step lp_refine        python3 lp_refine.py
step merge_lp         python3 thresholds.py --merge-lp
step verify_lp_thr    python3 verify_csv.py lp_threshold_members.csv
step region_diff      python3 region_diff.py
step members          python3 members_export.py
step verify_members   python3 verify_csv.py threshold_members.csv
step lp_relaxed       python3 lp_relaxed.py
step mixed            python3 run_mixed.py
step rho_check        python3 rho_check.py
step rho_verify       python3 rho_verify.py
step verify_rho       python3 verify_csv.py rho_check_eq.csv
step collapse         python3 run_collapse.py
step theory_test      python3 theory_test.py
step forcing_test     python3 forcing_test.py
step kscan            python3 kscan.py
step klow             python3 klow.py
step render           python3 render.py
echo "$(date +%H:%M:%S) all steps done" >> run_all.log
