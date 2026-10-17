#!/bin/sh
# Full-size rerun of every experiment in this repository, as published (same scripts, same arguments, same seeds).
#
#   sh validation/run_all.sh gpu   # GPU experiments (~9 h on an RTX 5060 laptop GPU)
#   sh validation/run_all.sh cpu   # CPU experiments (~45 min)
#
# Run inside a container whose /lab is a WORKING COPY of this repository's lab/ directory (the scripts read and write
# absolute /lab/cipher/... paths and overwrite their result files there), with /val mounted for logs. Never point /lab
# at the published copy: compare.py reads the published results from a separate, read-only clone.
# Prerequisites: the two Christie novels in lab/cipher/lm/corpus/ and lab/cipher/grille/model_text_big.txt rebuilt
# (README "Reproduce"). Each step logs its command, stdout+stderr, exit code and elapsed seconds to /val/logs/.
set -u
MODE=${1:-gpu}
LOG=/val/logs
mkdir -p "$LOG"
cd /lab/cipher
step() {   # step NAME COMMAND...
  name=$1; shift
  start=$(date +%s)
  echo "$*" > "$LOG/$name.cmd"
  "$@" > "$LOG/$name.log" 2>&1
  code=$?
  end=$(date +%s)
  echo "{\"step\": \"$name\", \"exit\": $code, \"seconds\": $((end - start)), \"command\": \"$*\"}" >> "$LOG/steps-$MODE.jsonl"
}
if [ "$MODE" = gpu ]; then
  step F71_bench2            python grille/bench2.py
  step F78_bench_ngram       python grille/bench_ngram.py
  step F74_bench_tolerance   python grille/bench_tolerance.py
  step I47_table_validate    python round11/table_test.py validate
  step F76_identifiability_A python round11/identifiability.py A 100 182,273,364,455,546,728,1092 -val
  step F76_identifiability_B python round11/identifiability.py B 100 182,273,364,455,546,728,1092 -val
  step F77_robustness        python round12/review_checks.py ident 50 182,273,364,546 -val
  step F79_comparability     python round12/comparability.py -val
else
  step R35_digraph_5x5       python round11/micro_digraph_cells.py 2000
  step R35_digraph_4x5       python round11/micro_digraph_cells_4x5.py
  step O34_fsq_search        python round12/review_checks.py fsq 100 10 -val 50000
  step O34_fsq_order         python round12/fsq_order.py 2000
fi
echo "done $MODE" >> "$LOG/steps-$MODE.jsonl"
