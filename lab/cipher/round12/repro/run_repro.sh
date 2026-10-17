#!/bin/sh
# Clean-room reproduction of the report's headline experiments, from a fresh copy of the repository
# (README "Reproduce" commands; same seeds; smaller sizes where noted). No network. Results: /lab/cipher/*/...-repro.json
set -x
cd /lab/cipher
date -u +%F > /lab/repro-started.txt
python grille/bench_ngram.py                                                   > /lab/repro-bench_ngram.log 2>&1    # F73 (full size)
cp grille/bench-ngram.json grille/bench-ngram-repro.json
python round11/identifiability.py A 20 182,546 -repro                          > /lab/repro-ident-A.log 2>&1        # F76, first 20 plants
python round11/identifiability.py B 20 182,546 -repro                          > /lab/repro-ident-B.log 2>&1
python round12/review_checks.py ident 10 182,546 -repro                        > /lab/repro-review-ident.log 2>&1   # F77, first 10 plants
python round12/review_checks.py fsq 30 10 -repro 50000                         > /lab/repro-fsq.log 2>&1            # O33, first 30 passages
python round12/fsq_order.py 2000                                               > /lab/repro-fsq-order.log 2>&1      # O33 order test (reads fsq-full.json)
date -u +%F > /lab/repro-finished.txt
