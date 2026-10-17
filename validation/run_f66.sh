#!/bin/sh
# F66: rerun Friedman's replication of Hendrick's 30-statistic "no message" test N times (default 20).
# The script (validation/f66/hendrick_familywise.py, unmodified, SHA-256 eab906a2...) draws its 1,000 dealings without
# a seed and writes to an absolute workspace path, so each rerun uses a copy whose output path is redirected to OUTDIR.
#   sh validation/run_f66.sh OUTDIR [N]      (python with numpy; ~7 s per rerun)
set -eu
OUT=$1; N=${2:-20}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
sed 's#/workspace/research/cipher/dagapeyeff/round9/friedman/familywise_complete.json#familywise_rerun.json#' \
    "$HERE/f66/hendrick_familywise.py" > "$OUT/hendrick_familywise_rerun.py"
cd "$OUT"
i=1
while [ "$i" -le "$N" ]; do
  python hendrick_familywise_rerun.py > "rep$i.log" 2>&1
  mv familywise_rerun.json "rep$i.json"
  i=$((i + 1))
done
