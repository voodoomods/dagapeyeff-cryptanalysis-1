"""F4 as originally computed (developer session, October 11, 2026) - the command recorded in the session log, unchanged
except that it reads data/ciphertext.txt (its first 392 digits are identical to the cleaned.txt it read then).

Statistic: for each period p = 2..20, the largest share of the eight rare occurrences on one residue mod p, minus 1/p;
take the maximum over p. Null: the eight positions are a uniformly random 8-subset of the 196 positions (seeded,
random.Random(t) for t = 0..19,999). Reported: (n + 1) / (N + 1), n = placements scoring at least the real value.

    python validation/original/f4_original.py      (standard library only)
"""
import random
from pathlib import Path
s = "".join(c for c in (Path(__file__).resolve().parents[2] / "data" / "ciphertext.txt").read_text() if c.isdigit())
pairs = [s[i:i+2] for i in range(0, len(s)-1, 2)][:196]
rare = [i for i, p in enumerate(pairs) if p in ('71','92','93','94','04')]
print("positions (0-based, 04 kept):", rare)
print("mod 14:", [i % 14 for i in rare], "| mod 7:", [i % 7 for i in rare], "| mod 2:", [i % 2 for i in rare])
# chance: 8 positions all on one residue, best over periods 2..20 (max-statistic null)
def best(pos):
    return max(max(__import__('collections').Counter(i % p for i in pos).values()) / len(pos) - 1/p for p in range(2, 21))
real = best(rare); n = 0; N = 20000
for t in range(N):
    if best(random.Random(t).sample(range(196), len(rare))) >= real: n += 1
print("share of random placements as aligned (any period 2-20):", (n + 1) / (N + 1))
