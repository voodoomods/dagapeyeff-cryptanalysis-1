# Addendum to FINDINGS.md (October 15, 2026)

`FINDINGS.md` is the team's write-up as it stood on October 13 and is kept unchanged as evidence. Two of its
"other engines" read as if computing time were the obstacle ("UNTESTABLE at this length ... at budgets up to
1200s"). The evidence points elsewhere:

- **Grille + polyphonic table (F68, I44):** even with the grille given, a wrong table outscores the true one in 89%
  of practice ciphers at 182 symbols (F76), and in 74-92% under every model and score of the October 15 checks
  (F77). Additional optimization of the same objective therefore cannot be assumed to improve true-table
  recovery; how success rates change with longer search budgets has not been established.
- **Double transposition (R20) and columnar transposition (R21-R27) with a one-to-one key:** excluded by the symbol
  counts for any transposition (C9, Hendrick 2026). With a polyphonic table, F76 applies: the table is undetermined
  even when the order is known.
- **Four-square / two-square (R32, F50):** with random keys, excluded by symbol usage (R35) - they spread English
  over 18-25 distinct symbols in 182 (0 of 10,000 practice ciphers at 13 or fewer); the message uses 13. Scripts and
  results: `lab/cipher/round11/micro_digraph_cells.py`, `micro_digraph_cells_4x5.py` and their `.json` results.
  A key built on purpose around the message is NOT excluded: it reached 13 flat symbols in 13 of 100 passages, 10 of
  them not flagged by the tested order statistic at the 5% level (O34,
  `lab/cipher/round12/`). That construction has not been searched.

See the report, Section 7, "Is it a question of computing time?"
