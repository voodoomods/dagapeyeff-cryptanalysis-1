# QA report — DAgapeyeff-Report-VoodooMods.pdf

**Verdict: PASS WITH NOTES** (developer, 2026-10-14; juran's run t-8c86314a was canceled after its model calls on
DeepSeek-V3.2 took ~3 min each and timed out — see the separate platform task).

Method: the PDF's text (`report.txt`, pdftotext) checked programmatically and by reading against `SOURCE-PACK.md`,
`figs/fig6_data.json` and the fact-check log; every page rendered and inspected.

| Check | Result |
|---|---|
| Identifiability numbers (exec summary, §6.4 table, §7, §8, Figure 6) agree with `fig6_data.json` and F76 | OK — corpus rows exact; see note 1 |
| Counts "x of y" (6 of 6, 2 of 6, 4/4, 1/4, 2/4, 0 of 12, 178 of 200, 0 of 3, 364 / 368 of 1,000) | OK — F73, F74, F76, F68, F31 |
| p-values 0.73, 0.91, 0.28, 0.29; 1 in 20,000; 479,051; 85–90 % | OK — F31, F32, C9/F66, F4, R29 |
| 50 % crossing ≈ 420 symbols; no "500–700" | OK — interpolated from 41 % (364) and 57 % (455) |
| Novelty claims match §9 | OK — "new as far as checked" only for F73, F74 (polyphonic), F76 |
| Overclaiming words (first / solved / proved / decipher) | OK — every use literal or hypothetical; "We claim no decipherment" |
| Figures: 6 present, numbered, captioned, drawn from result files | OK |
| Layout: no clipped figures, no split tables, cover without running header | OK |

**Notes**

1. The combined curve at 273 and 728 symbols is exactly 26.5 % and 74.5 %; the report, case entry F76 and executive
   summary round half-up to 27 % and 75 %. Consistent throughout; Python's default rounding would give 26 % / 74 %.
2. Section 6.3's repair experiment rests on 2 practice ciphers; the report says so in §8 and relies on §6.4 (200) for
   the conclusion.
3. RESOLVED (second pass): the unsourced sentence that D'Agapeyeff later could not read the cipher was removed.

**Second pass (rebuild with appendices A–C and rights notices):** every case entry the report cites is confirmed and
none rests on a disputed one (O23 confirmed against Hendrick's full text); all numbers re-checked against the final
text; Barker volume/issue dropped (not verifiable); glossary corrected (coordinate grid of row digits 6–9 and 0, column
digits 1–5, not a 5 × 5 square); every Appendix C fingerprint verified identical in the repository
(`release/build_release.py`), and `sha256sum -c MANIFEST.sha256` passes for all 73 files.
