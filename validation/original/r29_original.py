"""R29 as originally run (developer session, October 11, 2026) - the command recorded in the session log, unchanged.

Needs the PegasusDMZ agent code at commit c908608 (app.poly_engine, app.compound_ciphers._lang_stream,
app.flatness_tools.message), which is not part of this repository: run from that tree's agent-image/ directory.
Rerun on October 17, 2026 at c908608 in a container with no network: output identical to the original -
  REAL message lag-1 MI p = 0.698
  planted polyphonic (no transposition): lag-1 MI p<0.05 in 40 /40; p<0.01 in 39 /40; median p 0.0

Design: one random.Random(9) stream for everything; the real message is tested first; then 40 practice texts of 182
letters, text t = word-frequency stream letters 120,000 + 1,500 t onward; each through its own balanced 13-group table
built from the stream's first 100,000 letters; lag-1 mutual information (nats) against 400 shuffles; p = share of
shuffles at least as large (no +1).
"""

import random,math,numpy as np
from collections import Counter
from app import poly_engine as pe
from app.compound_ciphers import _lang_stream
from app.flatness_tools import message
s=_lang_stream('en'); rnd=random.Random(9)
def mi(x,k=1):
  n=len(x)-k; pr=Counter(zip(x[:-k],x[k:])); a=Counter(x[:-k]); b=Counter(x[k:])
  return sum(c/n*math.log(c*n/(a[u]*b[v])) for (u,v),c in pr.items())
def pval(x,sh=400):
  r=mi(x); y=list(x); null=[]
  for _ in range(sh): rnd.shuffle(y); null.append(mi(y))
  return np.mean(np.array(null)>=r)
real=message('dagapeyeff'); print('REAL message lag-1 MI p =',round(pval(real),3))
ps=[]
for t in range(40):
  txt=s[120000+t*1500:120000+t*1500+182]; tab=pe.balanced_table(s[:100000],13,rnd)
  ps.append(pval([tab[ord(c)-65] for c in txt]))
ps=np.array(ps); print('planted polyphonic (no transposition): lag-1 MI p<0.05 in',int((ps<0.05).sum()),'/40; p<0.01 in',int((ps<0.01).sum()),'/40; median p',round(float(np.median(ps)),4))
