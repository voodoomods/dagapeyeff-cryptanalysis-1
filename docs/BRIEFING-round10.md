# D'Agapeyeff — Round 10 briefing: get the key

From the developer (Claude), 2026-10-14. CONFIDENTIAL — nothing leaves the pod. Read the new entries first: F71, I46,
O32 (and C9, F31, F32, R29, F34). The case card is compact now — one line per entry; `case_file` has full text.

## Where the round starts

- **The grille search works once the key is right.** With the key given, every planted grille is recovered exactly
  (GPU 3/3, 49/49 orbits). Earlier "0/3" results were a judging bug: a grille turned a quarter is the SAME solution
  (case F71). With the key unknown: no power (the field's wall too).
- **For the real cipher "the key" is the polyphonic table** (13 symbols, each a balanced group of letters): a one-to-one
  key on natural text is already excluded by the counts (F31, C9).
- **Table given, the grille is partly solvable**: score orders by group-symbol quadgrams (`grille_engine.group_quadgrams`)
  — one plant solved 48/49, another stuck because a wrong order outscored the true one (I46). The developer builds
  higher-order group n-grams (13⁵, 13⁶ are cheap) now.
- **A key signal exists without the grille**: 14–37% of horizontally adjacent cells are consecutive plaintext letters,
  so neighbour pairs rank keys (O32) — weak so far (beats frequency-only in 4/6 plants).

## Tracks (each task carries only its toolset — cheaper calls)

| # | Track | Pair | Toolset |
|---|---|---|---|
| K0 | **Clear the proposal backlog** (62 waiting): confirm what the claim gate passes and the evidence supports; retire the rest | turing | stats |
| K1 | **The threshold**: how right must the key (one-to-one) or the table (polyphonic) be before the grille search locks on? Corrupt the true key/table to 50–95% and measure recovery | welchman + painvin | gpu |
| K2 | **Recover the key from the grid**: strengthen the neighbour-pair statistic — horizontal, vertical, diagonal, distance-2, wrap-around; which relations carry consecutive-plaintext signal under a turning grille; build the combined likelihood; key accuracy vs frequency-only on plants | kasiski + friedman | stats |
| K3 | **Recover the TABLE**: the same for polyphonic tables — accuracy measured as letter pairs grouped correctly; can count balance + neighbour pairs narrow the table to a handful? | rejewski + ventris | stats |
| K4 | **The book on keys**: the keys, keywords and tables the book itself uses or shows; any table with two letters per cell; any grille instructions (size, nulls) | kahn | book |

**turing** leads: K0 first, then the checkpoint and round10/SUMMARY.md.

## How to work

- Lab scripts may import the engines: copy `/app/app/grille_engine.py` and `poly_engine.py` beside your script under
  `/lab/cipher/round10/<you>/`; plants: `grille_engine.plant(text, True, rng)` (one-to-one) and
  `grille_engine.plant_poly(text, table, True, rng)` with `poly_engine.balanced_table(text, 13, rng)`; search:
  `grille_engine.anneal(Q, cells, chains, 0, seed, True, key=..., steps=N)`; judge with
  `grille_engine.match_up_to_rotation(found_shifts, true_shifts)` — NEVER raw orbit counts.
- Order statistics vs shuffles: `perm_test` only; report the family-wise p.
- Work together: team_read first; plan + idea for your partner; consult your partner; post results as they land with
  files; team_read before finishing. Don't install packages. After a lab job END THE TURN.
