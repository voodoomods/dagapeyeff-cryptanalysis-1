#!/usr/bin/env python3
"""Verify every row of Appendix E against ident-full.json."""
import json
import math


def wilson_ci(count, n):
    if n == 0: return (0, 0, 0)
    p = count / n
    z = 1.96; z2 = z*z
    denom = 1 + z2/n
    center = (p + z2/(2*n)) / denom
    margin = z * math.sqrt((p*(1-p) + z2/(4*n)) / n) / denom
    return p, max(0, center - margin), min(1, center + margin)

def fmt_ci(lo, hi): return f'{round(lo*100)}–{round(hi*100)}%'

with open('/lab/cipher/round12/ident-full.json') as f: idf = json.load(f)

# Model mapping: (source, corpus_key) → model
joint6_map = {('pool', "A'"): 'A:joint6', ('pool', 'B'): 'B:joint6',
              ('prose', "A'"): 'A:joint6', ('prose', 'B'): 'B:joint6',
              ('prose', 'AB'): 'C:joint6'}

# chain-rule: (source, corpus_key, score_desc) → model
chain_map = {('prose', "A'", 'cr5'): 'A:cond6', ('prose', 'B', 'cr5'): 'B:cond6',
             ('prose', 'AB', 'cr3'): 'C:cond4', ('prose', 'AB', 'cr4'): 'C:cond5',
             ('prose', 'AB', 'cr5'): 'C:cond6'}

# Appendex E rows
appendix = [
    ('pool', "A'", 'j6', 182, 13, 50, 26, '16–40%', 37, 23, 1),
    ('pool', "A'", 'j6', 273, 21, 50, 42, '29–56%', 29, 11, 2),
    ('pool', "A'", 'j6', 364, 22, 50, 44, '31–58%', 28, 9,  2),
    ('pool', "A'", 'j6', 546, 28, 50, 56, '42–69%', 22, 13, 5),
    ('pool', 'B',  'j6', 182, 10, 50, 20, '11–33%', 40, 33, 8),
    ('pool', 'B',  'j6', 273, 13, 50, 26, '16–40%', 37, 27, 10),
    ('pool', 'B',  'j6', 364, 19, 50, 38, '26–52%', 31, 23, 7),
    ('pool', 'B',  'j6', 546, 30, 50, 60, '46–72%', 20, 14, 2),
    ('prose', "A'", 'j6', 182, 9, 50, 18, '10–31%', 41, 29, 7),
    ('prose', "A'", 'j6', 273, 14, 50, 28, '17–42%', 36, 28, 7),
    ('prose', "A'", 'j6', 364, 14, 50, 28, '17–42%', 36, 24, 7),
    ('prose', "A'", 'j6', 546, 25, 50, 50, '37–63%', 25, 15, 7),
    ('prose', 'B',  'j6', 182, 6, 50, 12, '6–24%', 44, 32, 6),
    ('prose', 'B',  'j6', 273, 13, 50, 26, '16–40%', 37, 28, 12),
    ('prose', 'B',  'j6', 364, 14, 50, 28, '17–42%', 36, 27, 10),
    ('prose', 'B',  'j6', 546, 22, 50, 44, '31–58%', 28, 23, 5),
    ('prose', "A'", 'cr5', 182, 6, 50, 12, '6–24%', 44, 26, 8),
    ('prose', "A'", 'cr5', 273, 12, 50, 24, '14–37%', 38, 20, 7),
    ('prose', "A'", 'cr5', 364, 14, 50, 28, '17–42%', 36, 21, 4),
    ('prose', "A'", 'cr5', 546, 15, 50, 30, '19–44%', 35, 21, 11),
    ('prose', 'B',  'cr5', 182, 8, 50, 16, '8–29%', 42, 28, 7),
    ('prose', 'B',  'cr5', 273, 14, 50, 28, '17–42%', 36, 23, 11),
    ('prose', 'B',  'cr5', 364, 16, 50, 32, '21–46%', 34, 19, 6),
    ('prose', 'B',  'cr5', 546, 25, 50, 50, '37–63%', 25, 15, 5),
    ('prose', 'AB', 'cr3', 182, 4, 50, 8, '3–19%', 46, None, 4),
    ('prose', 'AB', 'cr3', 273, 5, 50, 10, '4–21%', 44, None, 9),
    ('prose', 'AB', 'cr3', 364, 8, 50, 16, '8–29%', 42, None, 11),
    ('prose', 'AB', 'cr3', 546, 15, 50, 30, '19–44%', 35, None, 7),
    ('prose', 'AB', 'cr4', 182, 4, 50, 8, '3–19%', 46, None, 11),
    ('prose', 'AB', 'cr4', 273, 7, 50, 14, '7–26%', 43, None, 10),
    ('prose', 'AB', 'cr4', 364, 10, 50, 20, '11–33%', 40, None, 9),
    ('prose', 'AB', 'cr4', 546, 14, 50, 28, '17–42%', 36, None, 3),
    ('prose', 'AB', 'cr5', 182, 5, 50, 10, '4–21%', 45, None, 16),
    ('prose', 'AB', 'cr5', 273, 17, 50, 34, '22–48%', 33, None, 8),
    ('prose', 'AB', 'cr5', 364, 16, 50, 32, '21–46%', 34, None, 8),
    ('prose', 'AB', 'cr5', 546, 18, 50, 36, '24–50%', 32, None, 6),
    ('prose', 'AB', 'j6',  182, 8, 50, 16, '8–29%', 42, None, 14),
    ('prose', 'AB', 'j6',  273, 12, 50, 24, '14–37%', 38, None, 13),
    ('prose', 'AB', 'j6',  364, 14, 50, 28, '17–42%', 36, None, 10),
    ('prose', 'AB', 'j6',  546, 15, 50, 30, '19–44%', 35, None, 6),
]

mismatches = 0
for row in appendix:
    src, corp, score_type, L, e_kept, e_total, e_pct, e_ci, e_found, e_other, e_fresh = row
    if score_type == 'j6':
        model = joint6_map[(src, corp)]
    else:
        model = chain_map[(src, corp, score_type)]

    runs = [r for r in idf['runs'] if r['source']==src and r['model']==model and r['L']==L]
    d_kept = sum(1 for r in runs if not r['truth_beaten'])
    d_total = len(runs)
    d_pct = round(100*d_kept/d_total)
    _, d_lo, d_hi = wilson_ci(d_kept, d_total)
    d_ci = fmt_ci(d_lo, d_hi)
    d_beaten = sum(1 for r in runs if r['truth_beaten'])
    
    row_id = f'{src}/{corp}/{score_type}/L={L}'
    ok = True
    if d_kept != e_kept or d_pct != e_pct:
        print(f'MISMATCH kept: {row_id} | report={e_kept}/{e_total}={e_pct}% | data={d_kept}/{d_total}={d_pct}%')
        ok = False
    if d_ci != e_ci:
        print(f'MISMATCH CI:   {row_id} | report={e_ci} | data={d_ci}')
        ok = False
    if d_beaten != e_found:
        print(f'MISMATCH found: {row_id} | report={e_found} | data={d_beaten}')
        ok = False
    # For L=182, check other/fresh
    if L == 182:
        oc_runs = [r for r in runs if r.get('other_found_minus_truth') is not None]
        oc_beats = sum(1 for r in oc_runs if r['other_found_minus_truth'] > 0)
        if e_other is not None and oc_beats != e_other:
            print(f'MISMATCH other: {row_id} | report={e_other} of {e_found} | data={oc_beats} of {len(oc_runs)}')
            ok = False
        fp_runs = [r for r in runs if r.get('fresh_found_minus_truth') is not None]
        fp_beats = sum(1 for r in fp_runs if r['fresh_found_minus_truth'] > 0)
        if fp_beats != e_fresh:
            print(f'MISMATCH fresh: {row_id} | report={e_fresh} of {e_found} | data={fp_beats} of {len(fp_runs)}')
            ok = False
    if ok:
        print(f'OK: {row_id}')
    else:
        mismatches += 1

print(f'\nApp E total mismatches: {mismatches}')
