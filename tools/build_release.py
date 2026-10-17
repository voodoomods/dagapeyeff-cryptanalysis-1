"""Assemble the GitHub folder `dagapeyeff-cryptanalysis-1` from the lab and the evidence archive, byte for byte.

Run in the agent container:  python /workspace/research/cipher/dagapeyeff/release/build_release.py
Output: /workspace/research/cipher/dagapeyeff/release/dagapeyeff-cryptanalysis-1/
  - mirrors the lab layout (lab/cipher/...) so every experiment script runs unchanged and keeps its SHA-256;
  - writes MANIFEST.sha256 (every file) and evidence/APPENDIX-C.md (the report's appendix: each evidence file, its
    fingerprint, and where it is in the repository — or why it is listed by fingerprint only);
  - verifies every file of the evidence manifest is present with an IDENTICAL hash; exits 1 if not.
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

LAB = Path("/lab/cipher")
WS = Path("/workspace/research/cipher/dagapeyeff")
EV = WS / "evidence"
REPO = WS / "release" / "dagapeyeff-cryptanalysis-1"
OWNER, AUTHOR, YEAR = "VoodooMods LLC", "Nicolas Houghtaling", 2026
DOI = "10.5281/zenodo.23306263"
ORCID = "0009-0001-3192-544X"
FINAL = os.environ.get("PEGASUS_FINAL") == "1"

# evidence path (as in evidence/MANIFEST.md) -> repository path; None = fingerprint only, not redistributed (reason)
MAP = {
    "case/dagapeyeff.json": "evidence/case/dagapeyeff.json",
    "jobs/lab_jobs.json": "evidence/jobs/lab_jobs.json",
    "docs/FINDINGS.md": "docs/FINDINGS.md",
    "docs/BRIEFING-round10.md": "docs/BRIEFING-round10.md",
    "docs/literature/NOVELTY-CHECK-2026-10-14.md": "docs/literature/NOVELTY-CHECK-2026-10-14.md",
    "docs/literature/novelty-search-2026-10-14.json":
        (None, "literature search results incl. 31 third-party abstracts — not redistributed; titles, authors, years and DOIs are in docs/literature/novelty-search-2026-10-14.metadata.json"),
    "docs/literature/gariazzo2026/Report_Agapeyeff.pdf": "docs/literature/gariazzo2026/Report_Agapeyeff.pdf",
    "docs/literature/hendrick2026/paper/dagapeyeff-exclusions.pdf":
        (None, "Hendrick 2026 manuscript — all rights reserved by its author; cite doi:10.5281/zenodo.23241303"),
    "sources/kahn_snippets.json":
        (None, "extracts from D'Agapeyeff's 1939 book (archive.org full-text search) — not redistributed"),
}
# Corpus novels public domain in the USA but still in copyright elsewhere (Agatha Christie, d. 1976): listed with
# fingerprints in lab/cipher/lm/CORPUS.md, not redistributed. model_text_big.txt contains their text, so it is rebuilt
# from the corpus with tools/build_model_text.py instead of being shipped.
NOT_REDISTRIBUTED = {"mysterious-affair-styles.txt", "secret-adversary.txt"}
CORPUS = [  # file, title, author, first published
    ("adventures-holmes.txt", "The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 1892),
    ("great-expectations.txt", "Great Expectations", "Charles Dickens", 1861),
    ("hound-baskervilles.txt", "The Hound of the Baskervilles", "Arthur Conan Doyle", 1902),
    ("man-who-was-thursday.txt", "The Man Who Was Thursday", "G. K. Chesterton", 1908),
    ("memoirs-holmes.txt", "The Memoirs of Sherlock Holmes", "Arthur Conan Doyle", 1894),
    ("mysterious-affair-styles.txt", "The Mysterious Affair at Styles", "Agatha Christie", 1920),
    ("return-holmes.txt", "The Return of Sherlock Holmes", "Arthur Conan Doyle", 1905),
    ("secret-adversary.txt", "The Secret Adversary", "Agatha Christie", 1922),
    ("secret-agent.txt", "The Secret Agent", "Joseph Conrad", 1907),
    ("tale-of-two-cities.txt", "A Tale of Two Cities", "Charles Dickens", 1859),
    ("time-machine.txt", "The Time Machine", "H. G. Wells", 1895),
    ("war-and-peace.txt", "War and Peace (Project Gutenberg English translation)", "Leo Tolstoy", 1869),
    ("war-of-the-worlds.txt", "The War of the Worlds", "H. G. Wells", 1898),
]
LAB_FILES = [  # (lab path relative to /lab/cipher) — copied to lab/cipher/<same>
    "grille/grille_engine.py", "grille/poly_engine.py",
    "grille/bench2.py", "grille/bench_ngram.py", "grille/bench_tolerance.py",
    "grille/bench-2.json", "grille/bench-ngram.json", "grille/bench-tolerance.json",
    "grille/plain_pool.txt", "grille/quad_en.npy",
    "grille/digraph_engine.py", "round11/micro_digraph_cells.py", "round11/micro_digraph_cells_4x5.py",
    "round11/micro-digraph-cells.json", "round11/micro-digraph-cells-4x5.json",
    "round11/table_test.py", "round11/identifiability.py", "round11/real_cells.json", "round11/cell_ids.json",
    "round11/validate.json", "round11/identifiability-A.json", "round11/identifiability-B.json",
    "round11/identifiability-A-big.json", "round11/identifiability-B-big.json",
    "round12/review_checks.py", "round12/fsq_order.py", "round12/ident-small.json", "round12/ident-full.json",
    "round12/fsq-small.json", "round12/fsq-full.json", "round12/fsq-order.json",
    "round12/comparability.py", "round12/comparability.json",
    "round12/repro/run_repro.sh", "round12/repro/compare_repro.py", "round12/repro/repro-compare.json",
    "round12/repro/bench-ngram-repro.json", "round12/repro/identifiability-A-repro.json",
    "round12/repro/identifiability-B-repro.json", "round12/repro/ident-repro.json", "round12/repro/fsq-repro.json",
    "round12/repro/fsq-order-repro.json",
    "audit/audit_fsq.py", "audit/label_audit.py", "audit/ngram_indep.py", "audit/label_full.py", "audit/test_label_distance.py",
    "audit/audit_fsq.json", "audit/label_audit.json", "audit/ngram_indep.json", "audit/label_full.json",
    "lib/label_distance.py", "lib/test_label_distance.py",
    "provenance/latin_flatness.py", "provenance/latin_flatness.json",
] + [f"lm/corpus/{p.name}" for p in sorted((LAB / "lm/corpus").glob("*.txt")) if p.name not in NOT_REDISTRIBUTED]
REPORT_FILES = ["front.md", "body_final.md", "back.md", "codes.md", "appendix-e.md", "make_appendix_e.py", "appendix-f.md", "make_appendix_f.py", "AUDIT-proof.md", "audit_appendix_e.py", "report.css", "build_report.py", "make_figures.py",
                "FACTCHECK-LOG.md", "QA-REPORT.md", "SOURCE-PACK.md", "DAgapeyeff-Report-VoodooMods.pdf"]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def put(src: Path, rel: str):
    dst = REPO / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def write(rel: str, text: str):
    dst = REPO / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.lstrip("\n"), encoding="utf-8")


def main():
    if REPO.exists():
        shutil.rmtree(REPO)
    REPO.mkdir(parents=True)
    for rel in LAB_FILES:
        put(LAB / rel, f"lab/cipher/{rel}")
    for name in REPORT_FILES:
        if (WS / "report" / name).exists():
            put(WS / "report" / name, f"report/{name}")
    for p in sorted((WS / "report" / "figs").glob("*")):
        put(p, f"report/figs/{p.name}")
    put(WS / "ciphertext.txt", "data/ciphertext.txt")
    for ev, dest in MAP.items():
        if isinstance(dest, str):
            put(EV / ev, dest)
    put(EV / "collect.py", "evidence/collect.py")
    put(WS / "release" / "build_model_text.py", "tools/build_model_text.py")
    put(WS / "release" / "sources.json", "docs/sources.json")
    for f in ("README.md", "CRITERIA.md", "run_all.sh", "compare.py", "flatness_standalone.py", "recompute_extra.py",
              "run_f66.sh", "f66/hendrick_familywise.py", "collect_results.py", "qa_checks.py",
              "f4_events.py", "original/f4_original.py", "original/r29_original.py"):   # release-candidate validation of October 16
        put(WS / "validation" / f, f"validation/{f}")
    res = WS / "validation" / "results"
    for f in sorted(res.rglob("*")) if res.exists() else []:
        if f.is_file():
            put(f, f"docs/validation-2026-10-16/{f.relative_to(res).as_posix()}")
    res2 = WS / "validation" / "results-2026-10-17"     # R29 / F4 clarifications
    for f in sorted(res2.rglob("*")) if res2.exists() else []:
        if f.is_file():
            put(f, f"docs/validation-2026-10-17/{f.relative_to(res2).as_posix()}")
    for f in ("AUDIT-REPORT.md", "proposed.patch"):        # internal audit of October 15 (scripts/outputs: lab/cipher/audit/)
        put(WS / "audit-2026-10-15" / f, f"docs/audit-2026-10-15/{f}")
    write("docs/FINDINGS-ADDENDUM.md", chr(10).join([
        "# Addendum to FINDINGS.md (October 15, 2026)", "",
        "`FINDINGS.md` is the team's write-up as it stood on October 13 and is kept unchanged as evidence. Two of its",
        "\"other engines\" read as if computing time were the obstacle (\"UNTESTABLE at this length ... at budgets up to",
        "1200s\"). The evidence points elsewhere:", "",
        "- **Grille + polyphonic table (F68, I44):** even with the grille given, a wrong table outscores the true one in 89%",
        "  of practice ciphers at 182 symbols (F76), and in 74-92% under every model and score of the October 15 checks",
        "  (F77). Additional optimization of the same objective therefore cannot be assumed to improve true-table",
        "  recovery; how success rates change with longer search budgets has not been established.",
        "- **Double transposition (R20) and columnar transposition (R21-R27) with a one-to-one key:** excluded by the symbol",
        "  counts for any transposition (C9, Hendrick 2026). With a polyphonic table, F76 applies: the table is undetermined",
        "  even when the order is known.",
        "- **Four-square / two-square (R32, F50):** with random keys, excluded by symbol usage (R35) - they spread English",
        "  over 18-25 distinct symbols in 182 (0 of 10,000 practice ciphers at 13 or fewer); the message uses 13. Scripts and",
        "  results: `lab/cipher/round11/micro_digraph_cells.py`, `micro_digraph_cells_4x5.py` and their `.json` results.",
        "  A key built on purpose around the message is NOT excluded: it reached 13 flat symbols in 13 of 100 passages, 10 of",
        "  them not flagged by the tested order statistic at the 5% level (O34,",
        "  `lab/cipher/round12/`). That construction has not been searched.", "",
        "See the report, Section 7, \"Is it a question of computing time?\"", ""]))
    NL = chr(10)
    # literature search: metadata only (titles, authors, years, venues, DOIs - no abstracts)
    raw = json.loads((EV / "docs/literature/novelty-search-2026-10-14.json").read_text(encoding="utf-8"))
    meta = {k: {f: v.get(f) for f in ("title", "authors", "year", "venue", "doi", "url", "source", "citations")
                if v.get(f) is not None} for k, v in raw.items()}
    write("docs/literature/novelty-search-2026-10-14.metadata.json", json.dumps(meta, indent=1, ensure_ascii=False))
    write("docs/literature/gariazzo2026/ATTRIBUTION.md", NL.join([
        "Ruben Gariazzo (2026). *The D'Agapeyeff Cryptogram (1939): Anatomy, Reconstruction of a Solver, and Statistical",
        "Assessment.* Zenodo. doi:10.5281/zenodo.22011904. Licensed under Creative Commons Attribution 4.0 International",
        "(https://creativecommons.org/licenses/by/4.0/). Included unmodified. Not covered by this repository's copyright.", ""]))
    SRC = json.loads((WS / "release" / "sources.json").read_text(encoding="utf-8"))
    rows = ["# Language corpora", "",
            "Provenance of every external language text used in the study; the report's Appendix F has the same record "
            "with each text's role per experiment. Source of truth: `docs/sources.json`.", "",
            "## English novels (13)", "",
            f"Retrieved {SRC['retrieval']['date']} from `{SRC['retrieval']['url_pattern']}`; processing: "
            f"{SRC['retrieval']['transformation']}. Catalog details are quoted from each book's Project Gutenberg record "
            "(read 2026-10-16). 'First published' is a standard reference date, not taken from the files. The English "
            "language models are built from these novels; `tools/build_model_text.py` rebuilds "
            "`lab/cipher/grille/model_text_big.txt` from them and, with these exact files, reproduces the fingerprint below.", "",
            "| File | Work | Gutenberg eBook | Record: released / last update | First published | In this repository | SHA-256 |",
            "|---|---|---|---|---|---|---|"]
    for e in SRC["english"]:
        fn = e["file"]
        h = sha(LAB / "lm/corpus" / fn)
        who = e["author"] + (f", translated by {e['translator']}" if e["translator"] else "")
        inc = ("not redistributed - public domain in the USA, still in copyright in the UK and EU (author d. 1976); "
               "obtain from Project Gutenberg") if fn in NOT_REDISTRIBUTED else "yes - public domain in the USA"
        rows.append(f"| `{fn}` | *{e['title']}*, {who} | [{e['id']}](https://www.gutenberg.org/ebooks/{e['id']}) | "
                    f"{e['release']} / {e['last_update']} | {e['first_published']} | {inc} | `{h}` |")
    rows += ["", SRC["english_not_used"], "",
             "## Latin editions (10) - not redistributed", "",
             "Used only for the Latin comparison of case F31 / F80 (report Section 2). Same retrieval and processing as "
             "above; the Latin reader then drops lines that are mostly English. Obtain from Project Gutenberg.", "",
             "| File | Work | Gutenberg eBook | Record language | English apparatus | SHA-256 |", "|---|---|---|---|---|---|"]
    for e in SRC["latin"]:
        ed = f" (ed. {e['editor']})" if e["editor"] and "translator" not in e["editor"] else (f" ({e['editor']})" if e["editor"] else "")
        rows.append(f"| `{e['file']}` | *{e['title']}*, {e['author']}{ed} | [{e['id']}](https://www.gutenberg.org/ebooks/{e['id']}) | "
                    f"{e['record_language']} | {'yes' if e['english_apparatus'] else 'no'} | `{e['sha256']}` |")
    wf = SRC["wordfreq"]
    rows += ["", "## Word frequencies (wordfreq)", "",
             f"`plain_pool.txt`, `quad_en.npy` and the practice plaintexts quoted in `bench-2.json` are derived from "
             f"wordfreq {wf['version']}: {wf['wordlist']}. Code license {wf['code_license']}; data license "
             f"{wf['data_license']}. Cite: {wf['citation']}. Attribution terms: {wf['attribution_terms']}", ""]
    mt = sha(LAB / "grille/model_text_big.txt")
    rows += ["", f"`lab/cipher/grille/model_text_big.txt` (not redistributed - it contains the text of every novel above): "
             f"SHA-256 `{mt}`. Rebuild: `python tools/build_model_text.py lab/cipher/lm/corpus lab/cipher/grille/model_text_big.txt`.", ""]
    write("lab/cipher/lm/CORPUS.md", NL.join(rows))
    sys.path.insert(0, str(WS / "release"))
    import build_model_text
    rebuilt = hashlib.sha256(build_model_text.build(str(LAB / "lm/corpus")).encode()).hexdigest()
    problems_early = [] if rebuilt == mt else [f"model text rebuild mismatch ({rebuilt[:16]} vs {mt[:16]})"]

    put(Path(__file__), "tools/build_release.py")
    put(WS / "release" / "accounting.py", "tools/accounting.py")
    put(WS / "release" / "accounting-2026-10-14.json", "evidence/accounting-2026-10-14.json")

    # ── verify against the evidence manifest (the report's appendix) ──
    m = (EV / "MANIFEST.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{16})…` \|", m, re.MULTILINE)
    appendix, problems = [], list(problems_early)
    for ev_path, prefix in rows:
        if ev_path in MAP and not isinstance(MAP[ev_path], str):
            appendix.append((ev_path, prefix, None, MAP[ev_path][1]))
            continue
        if ev_path in MAP:
            repo_rel = MAP[ev_path]
        elif ev_path.startswith(("results/", "scripts/", "engines/")):
            repo_rel = "lab/cipher/" + ev_path.split("/", 1)[1]
        else:
            problems.append(f"no mapping for {ev_path}")
            continue
        f = REPO / repo_rel
        if not f.exists():
            problems.append(f"missing in repo: {repo_rel}")
            continue
        h = sha(f)
        if not h.startswith(prefix):
            problems.append(f"HASH MISMATCH {repo_rel}: repo {h[:16]} vs evidence {prefix}")
        appendix.append((ev_path, h, repo_rel, ""))

    lines = ["## Appendix C. Evidence", "",
             "The key results of this report come from the files below; other figures come from case-file entries (Appendix D). The SHA-256 fingerprint (first 16 hex digits shown; "
             "`MANIFEST.sha256` in the repository has them in full) identifies each file exactly, so a reader can confirm "
             "that a file is the one the report used. Paths are in the `dagapeyeff-cryptanalysis-1` repository (https://github.com/voodoomods/dagapeyeff-cryptanalysis-1).", "",
             "::: {.evidence}", "", "| File in the repository | SHA-256 (prefix) |", "|---|---|"]
    for ev_path, h, repo_rel, note in appendix:
        if repo_rel is None:
            lines.append(f"| *not redistributed:* {note} | `{h[:16]}…` |")
        else:
            lines.append(f"| `{repo_rel}` | `{h[:16]}…` |")
    lines += ["", ":::"]
    write("evidence/APPENDIX-C.md", "\n".join(lines) + "\n")
    (WS / "report" / "APPENDIX-C.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ── rights, licenses, docs ──
    write("COPYRIGHT", f"""
Copyright (c) {YEAR} {OWNER}. Author: {AUTHOR}.

WHAT IS CLAIMED. {OWNER} claims copyright in this project's own contribution, to the extent copyright subsists in it:
the report and its figures, the documents and records written for this project, the selection and arrangement of its
results and evidence, the research data the project produced, and the source code.

TERMS.
* report/, figures, results (lab/cipher/**/*.json), evidence/ and the documents in docs/ written for this project:
  licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0; LICENSE-CC-BY-4.0.md,
  https://creativecommons.org/licenses/by/4.0/). You may share and adapt them for any purpose, including
  commercially, provided you credit {AUTHOR} and {OWNER}, link to the license and indicate any changes.
* Source code (*.py): licensed under the Apache License, Version 2.0 (LICENSE). Copies and derivative works must keep
  this copyright notice and the attribution in NOTICE.

WHAT IS NOT CLAIMED.
* Third-party material, which keeps its own license — see NOTICE.
* Short quotations from other works (for example from A. D'Agapeyeff's *Codes and Ciphers*, 1939, and from published
  papers) reproduced in the case file and documents for criticism and review; they remain their owners' property.
* Facts, numbers and ideas as such, the ciphertext itself, and the names of historical figures used as names for the
  project's AI agents (which imply no association with, or endorsement by, those people or their estates).

AI ASSISTANCE. Much of the text and code was produced with AI systems (Anthropic's Claude, and AI agents running on
DeepSeek, Kimi and Qwen models) under the direction of {AUTHOR}. Rights are claimed only to the extent the law
recognizes them in such material.

No right is granted to the names "VoodooMods" or "PegasusDMZ", or to any other name or mark of {OWNER}.
""")
    write("NOTICE", f"""
dagapeyeff-cryptanalysis-1
Copyright (c) {YEAR} {OWNER}
Research conceived and directed by {AUTHOR}.

This product includes software developed by {OWNER} for the study "The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring" (doi:{DOI}). Any redistribution or
derivative work of the code must retain this NOTICE and credit {AUTHOR} and {OWNER}.

THIRD-PARTY MATERIAL INCLUDED (not covered by this repository's copyright):
* lab/cipher/lm/corpus/*.txt - 11 novels from Project Gutenberg (eBooks 35, 36, 98, 108, 834, 974, 1400, 1661, 1695,
  2600 and 2852; War and Peace in the translation by Louise and Aylmer Maude), retrieved 2026-10-11, Gutenberg license
  header and footer removed. Public domain in the USA per their Gutenberg records; status elsewhere not legally
  reviewed. Listed with fingerprints and catalog details in lab/cipher/lm/CORPUS.md and docs/sources.json.
* lab/cipher/grille/plain_pool.txt, lab/cipher/grille/quad_en.npy, and the short practice-cipher plaintexts quoted
  in lab/cipher/grille/bench-2.json - generated from word frequencies in the `wordfreq` package (version 3.1.1;
  Speer, R. (2022), rspeer/wordfreq, doi:10.5281/zenodo.7199437). wordfreq's code is Apache-2.0 and its data is
  licensed CC BY-SA 4.0; these derived files are shared under CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/),
  not under this repository's CC BY 4.0. wordfreq's English data includes SUBTLEX-US (Brysbaert & New 2009) and
  SUBTLEX-UK (van Heuven et al. 2014) - freely available data, credited here as its terms require - and Google Books
  Ngrams (http://books.google.com/ngrams), OpenSubtitles (http://www.opensubtitles.org/) and other sources listed in
  the wordfreq README.
* docs/literature/gariazzo2026/Report_Agapeyeff.pdf - R. Gariazzo (2026), CC BY 4.0, doi:10.5281/zenodo.22011904;
  included unmodified with attribution (see ATTRIBUTION.md beside it).
* docs/literature/novelty-search-2026-10-14.metadata.json - bibliographic metadata (titles, authors, years, venues,
  DOIs) from OpenAlex, Semantic Scholar and arXiv searches.
* data/ciphertext.txt - the challenge cipher printed in A. D'Agapeyeff, *Codes and Ciphers* (1939).

NOT INCLUDED (listed by fingerprint only):
* C. Hendrick (2026) manuscript - all rights reserved by its author; doi:10.5281/zenodo.23241303.
* Extracts from D'Agapeyeff's *Codes and Ciphers* (1939) retrieved by full-text search.
* The literature search results with their abstracts (the abstracts belong to their authors and publishers).
* Two corpus novels by Agatha Christie (Gutenberg eBooks 863 and 1155), public domain in the USA but in copyright in
  the UK and EU, and lab/cipher/grille/model_text_big.txt, which contains their text - rebuild with
  tools/build_model_text.py.
* Ten Latin editions from Project Gutenberg used for the Latin comparison (case F31 / F80) - listed with eBook numbers
  and fingerprints in lab/cipher/lm/CORPUS.md.
""")
    apache = Path("/usr/share/common-licenses/Apache-2.0")
    write("LICENSE", apache.read_text() if apache.exists() else
          "Apache License, Version 2.0 — full text: https://www.apache.org/licenses/LICENSE-2.0.txt\n"
          f"Applies to the source code (*.py) of this repository. Copyright (c) {YEAR} {OWNER}. See COPYRIGHT and NOTICE.\n")
    write("LICENSE-CC-BY-4.0.md", f"""
# Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) {YEAR} {OWNER}. Author: {AUTHOR}.

The report, figures, results, evidence and documents written for this project (everything in this repository except
the source code and the third-party material listed in NOTICE) are licensed under the Creative Commons Attribution
4.0 International license.

Full legal code: https://creativecommons.org/licenses/by/4.0/legalcode
Summary: https://creativecommons.org/licenses/by/4.0/

Attribution: "{AUTHOR} / {OWNER}, The D'Agapeyeff Cipher (1939), doi:{DOI}, licensed CC BY 4.0."

The source code (*.py) is licensed separately under the Apache License 2.0 (LICENSE).
""")
    write("CITATION.cff", f"""
cff-version: 1.2.0
message: "If you refer to this work, please cite it as below."
title: "dagapeyeff-cryptanalysis-1: code, data and evidence for The D'Agapeyeff Cipher (1939)"
authors:
  - family-names: Houghtaling
    given-names: Nicolas
    orcid: "https://orcid.org/{ORCID}"
    affiliation: "{OWNER}"
date-released: "2026-10-17"
doi: "{DOI}"
repository-code: "https://github.com/voodoomods/dagapeyeff-cryptanalysis-1"
url: "https://github.com/voodoomods/dagapeyeff-cryptanalysis-1"
identifiers:
  - type: doi
    value: "{DOI}"
    description: "The research preprint and its supporting material"
license:
  - CC-BY-4.0
  - Apache-2.0
copyright: "Copyright (c) {YEAR} {OWNER}. Report and data CC BY 4.0; code Apache-2.0."
preferred-citation:
  type: report
  status: preprint
  title: "The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring"
  authors:
    - family-names: Houghtaling
      given-names: Nicolas
      orcid: "https://orcid.org/{ORCID}"
      affiliation: "{OWNER}"
  institution:
    name: "{OWNER}"
  year: {YEAR}
  month: 10
  doi: "{DOI}"
""")
    write("requirements.txt", "numpy>=1.26\ntorch>=2.2\nscipy>=1.11\nmatplotlib>=3.8\n")
    write("README.md", f"""
# dagapeyeff-cryptanalysis-1

**The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring**

{AUTHOR}, independent researcher ([ORCID {ORCID}](https://orcid.org/{ORCID})) · {OWNER} · {YEAR}{'' if FINAL else ' · *pre-publication draft*'}

**Repository:** <https://github.com/voodoomods/dagapeyeff-cryptanalysis-1>

**DOI (reserved):** {DOI} — reserved on Zenodo for this work; it resolves once the Zenodo record is published.

**Publication status:** Research preprint. This manuscript has undergone internal verification and AI-assisted critical review but has not been formally peer-reviewed by an independent academic journal.

© {YEAR} {OWNER}. Report, results and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code:
Apache-2.0. See `COPYRIGHT`, `LICENSE`, `LICENSE-CC-BY-4.0.md` and `NOTICE`.

**License exceptions.** These files keep their own terms (details in `NOTICE`):

- `lab/cipher/grille/plain_pool.txt`, `lab/cipher/grille/quad_en.npy` and the practice plaintexts quoted in
  `lab/cipher/grille/bench-2.json` are derived from wordfreq data and are shared under
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), not CC BY 4.0. Credit: Speer (2022), SUBTLEX-US and
  SUBTLEX-UK.
- `lab/cipher/lm/corpus/*.txt` are Project Gutenberg texts that are public domain in the USA. They are not licensed by
  us, and their status elsewhere has not been legally reviewed.
- `docs/literature/gariazzo2026/` is R. Gariazzo's report (CC BY 4.0, by its author).
- `data/ciphertext.txt` is the 1939 challenge cipher, quoted from D'Agapeyeff's book.
- Not included: two Agatha Christie novels and the model text built from them, the ten Latin editions, Hendrick's
  manuscript and third-party abstracts. See `lab/cipher/lm/CORPUS.md` for how to obtain the texts.

## The study in brief

In 1939 Alexander D'Agapeyeff closed *Codes and Ciphers* with a 196-symbol challenge cipher that has never been read.
Prior work (Hendrick 2026) ruled out every one-to-one letter key combined with any transposition; among the
systems it left open is the turning grille. This study,
conceived and directed by {AUTHOR} over seven days (October 8–14, 2026) with an AI research team, and checked further
on October 15 after reviews of the draft by a separate AI system (ChatGPT, OpenAI), tested in depth one construction consistent with every observed property — a
14 × 14 turning grille over a *polyphonic* table, in which each of the cipher's 13 symbols stands for a group of letters.
All rates below are measured on practice ciphers with known keys.

- **With the true table supplied, practice-cipher grilles were recovered** — six-symbol scoring recovered at least 45
  of 49 orbits in six of six practice ciphers, five exactly (F78; a preliminary demonstration, not recovery of the
  historical grille).
- **The table must be essentially exact** — 6 or more misplaced letters: 0 of 12 (F74; preliminary).
- **Under the n-gram scores tested, 182 symbols rarely single out the table** — started at the true table with the
  order known, the search keeps it in only 11% of 200 practice ciphers (84% at 1,092 symbols; F76), and in 8–26%
  under every plaintext, corpus and score tried after review (F77; every setup in the report's Appendix E). The
  higher-scoring tables fit the passage, not English, and the scores are comparable across tables (F79).
- **Four-square and two-square with random keys do not fit** — in 10,000 practice ciphers they spread English over
  18–25 distinct symbols, never the message's 13 (R35); this excludes the randomly keyed constructions tested, under the
  tested plaintext, not every possible key.
- **A purpose-built four-square can match the cipher's symbol usage and flatness** — a key optimized for each
  passage reached 13 symbols with the specified frequency flatness in 13 of 100 passages; 10 of those 13 were not
  flagged by the tested family-wise order statistic at the 5% threshold, which is not evidence that they contain no
  order (O34). A feasibility demonstration with keys optimized using the plaintext, not evidence that D'Agapeyeff
  used four-square; it has not been searched.

With the methods tested, the grille hypothesis cannot be decided from the cipher's own text. For the tested
objectives, higher-scoring incorrect tables frequently exist even when the true order and table are supplied, so more
optimization of the same objective cannot be assumed to help; longer budgets were not studied, and a differently
designed search or model is not ruled out (report, Section 7). No decipherment is claimed. The full argument, prior work and limitations are in
the report.

## Start here

| File | What it is |
|---|---|
| `report/DAgapeyeff-Report-VoodooMods.pdf` | **The report** — findings, figures, prior work, limitations, the team, budget and timeline |
| `report/FACTCHECK-LOG.md` | Every correction made while checking the report against its sources |
| `evidence/case/dagapeyeff.json` | The case file: every result with its evidence and review history (codes such as F78, R29 — explained in the report's Appendix D) |
| `MANIFEST.sha256` | SHA-256 of every file in this repository |

## Contents

| Path | Contents |
|---|---|
| `report/` | The PDF; its Markdown sources (`front.md`, `body_final.md`, `back.md`, `codes.md`, `appendix-e.md`); figures (`figs/`); `make_figures.py` and `build_report.py`; the fact-check log, QA report and source pack |
| `lab/cipher/grille/` | The search engines (`grille_engine.py`, `poly_engine.py`), the grille benchmarks (`bench2.py`, `bench_ngram.py`, `bench_tolerance.py`) with their results, and the English model texts |
| `lab/cipher/round11/` | The table-repair (`table_test.py`) and identifiability (`identifiability.py`) experiments, the cipher as cells, and their results |
| `docs/sources.json`, `lab/cipher/lm/CORPUS.md` | Provenance of every language source: Project Gutenberg eBook numbers, catalog details, retrieval date and processing, fingerprints, wordfreq version and licensing (the report's Appendix F) |
| `lab/cipher/provenance/` | The Latin comparison of case F80 (`latin_flatness.py`, needs the PegasusDMZ agent tools) and its result |
| `lab/cipher/lib/` | For future experiments: `label_distance.py` — exact (optimal one-to-one) group-label distance as the default, the published greedy matching under a legacy name, and raw letterwise distance — with unit tests (`test_label_distance.py`). Not used by the published results |
| `docs/validation-2026-10-17/`, `validation/original/` | The R29 and F4 clarifications of October 17: the original commands for both, recovered from the session record and rerun unchanged, the two F4 events computed side by side (`validation/f4_events.py`), and `R29-F4-RESPONSE.md` |
| `validation/` and `docs/validation-2026-10-16/` | The release-candidate validation of October 16: full-size reruns of the published experiments from a fresh clone (`run_all.sh`), predeclared criteria (`CRITERIA.md`), the expected-output comparison (`compare.py`), standalone recomputations that need no PegasusDMZ code (`flatness_standalone.py`, `recompute_extra.py`, `run_f66.sh`), and the results: `REVIEW-RESPONSE.md`, `validation-results.json`, logs and the QA report |
| `lab/cipher/audit/` and `docs/audit-2026-10-15/` | The internal audit of October 15 (written within the project, not by an unaffiliated party): separately written checks of the four-square reconstruction, flatness and order tests, the n-gram score and ten truth-start runs, and greedy versus exact label matching on all 2,000 robustness runs; scripts and outputs, with the audit report and the patch it led to |
| `lab/cipher/round12/repro/` | A clean-room reproduction of the headline experiments from a fresh copy of this repository (`run_repro.sh`), and its run-by-run comparison with the published results (`compare_repro.py`, `repro-compare.json`) |
| `lab/cipher/round12/` | The checks made after review of the draft: robustness of the identifiability result and purpose-built four-square keys (`review_checks.py`), the four-square order test (`fsq_order.py`), and their results |
| `lab/cipher/lm/` | `corpus/`: 11 of the 13 public-domain novels the English models are built from; `CORPUS.md` lists all 13 with fingerprints |
| `evidence/` | The case file, lab job records, the report's Appendix C (`APPENDIX-C.md`), the budget totals (`accounting-2026-10-14.json`) and the evidence collector |
| `docs/` | The novelty check and literature search, Gariazzo's report (CC BY 4.0), the team's findings write-up and the round-10 briefing |
| `data/ciphertext.txt` | The 395 digits as published |
| `tools/` | `build_release.py` (assembles and verifies this repository) and `accounting.py` (recomputes the budget from the raw records) |

Some material is listed by fingerprint only and not included, because it is not ours to redistribute: Hendrick's
manuscript (all rights reserved — doi:10.5281/zenodo.23241303), extracts from D'Agapeyeff's book, the literature search
with its abstracts (the metadata is included), and two corpus novels by Agatha Christie that are public domain in the
USA but not in the UK and EU — together with `model_text_big.txt`, which contains their text. See `NOTICE`.

## Verify

```
sha256sum -c MANIFEST.sha256
```

Every fingerprint in the report's Appendix C appears in `MANIFEST.sha256`.

## Reproduce

First obtain the two Christie novels from Project Gutenberg into `lab/cipher/lm/corpus/` (file names and fingerprints
in `lab/cipher/lm/CORPUS.md`) and rebuild the model text — this reproduces its published fingerprint exactly:

```
python tools/build_model_text.py lab/cipher/lm/corpus lab/cipher/grille/model_text_big.txt
```

The scripts read and write absolute paths under `/lab/cipher/`, exactly as they ran. Mount this repository's `lab/`
directory at `/lab` in a container with Python 3.12, PyTorch, SciPy and a CUDA GPU (CPU works, slowly). The PyTorch
image has no SciPy, which four of the scripts import, so build a small image first (the published runs used Python
3.12.13, NumPy 2.5.2, SciPy 1.18.1 and PyTorch 2.11.0 with CUDA 12.8):

```
printf 'FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
RUN pip install "scipy>=1.11" "matplotlib>=3.8"
' | docker build -t dagapeyeff-env -
run() {{ docker run --rm --gpus all -v "$PWD/lab:/lab" -w /lab/cipher dagapeyeff-env "$@"; }}
run python grille/bench_ngram.py                                              # Figure 4 (F78)
run python grille/bench_tolerance.py                                          # Figure 5 (F74)
run python round11/table_test.py validate                                     # Section 6.3 (I47)
run python round11/identifiability.py A 100 182,273,364,455,546,728,1092 -big   # Figure 6 (F76)
run python round11/identifiability.py B 100 182,273,364,455,546,728,1092 -big
run python round12/review_checks.py ident 50 182,273,364,546 -full                # Section 6.5 (F77)
run python round12/review_checks.py fsq 100 10 -full 50000                         # Section 7 (O34)
run python round12/fsq_order.py 2000
run python round12/comparability.py                                              # Section 6.5, comparability (F79)
run sh -c "cd lib && python test_label_distance.py"                           # exact vs legacy label distance (unit tests, ~1 min)
run python audit/test_label_distance.py                                           # audit: greedy vs exact label matching (unit test)
run python audit/audit_fsq.py                                                     # audit: four-square rebuild, flatness, order test
run python audit/ngram_indep.py                                                   # audit: independent n-gram scorer, 10 truth-start runs
run python audit/label_full.py                                                    # audit: all 2,000 robustness runs, greedy vs exact
```

**One entry point.** `validation/run_all.sh` runs every experiment above at full size (`gpu`: about 9 hours on a
laptop RTX 5060; `cpu`: under an hour), logging each command, its output, exit code and elapsed time;
`validation/compare.py` then checks every printed number against the rerun and the published files. Run it in a
container whose `/lab` is a working copy of `lab/` (the scripts overwrite their result files) and whose `/val` holds
the logs; keep a second, untouched clone for `--ref`:

```
docker run --rm --gpus all --network none -v "$PWD/work/lab:/lab" -v "$PWD/val:/val"     -v "$PWD/validation/run_all.sh:/val/run_all.sh:ro" dagapeyeff-env sh /val/run_all.sh gpu
python validation/compare.py --ref lab/cipher --new work/lab/cipher --steps val/logs --out compare.json
pip install wordfreq==3.1.1 scipy && python validation/flatness_standalone.py --lang en    # F31: 364/1000
```

Seeds are fixed; GPU annealing is not bit-for-bit deterministic, so individual runs vary slightly while the aggregate
results hold. `grille_engine.py` is the final version and is backward compatible with the earlier benchmarks.
`report/make_figures.py` redraws every figure from the result files; `report/build_report.py` rebuilds the PDF.

## Credit and method

Conceived and directed by **{AUTHOR}** ({OWNER}), who designed the research platform it ran on, chose the problem,
and made the decisions that shaped it. Software, search engines, analyses and writing: Anthropic's Claude (Opus 5.5)
under the author's direction. Supporting investigation: a team of AI agents on DeepSeek, Kimi and Qwen models (Section
11 of the report introduces each). Draft review: ChatGPT (OpenAI), through ChatGPT Plus, at the author's
request, over several rounds — an AI review, not human peer review. Language-model cost for the agent team: about US$68 (`evidence/accounting-2026-10-14.json`).

**Review status.** The repository includes the original experiment records, project-internal reproduction results
(`lab/cipher/round12/repro/`), separately implemented numerical checks written by the developer, outside the
experiment code (`lab/cipher/audit/`), and a full-size rerun of the published experiments from a fresh clone of this
repository, in containers with no network (`docs/validation-2026-10-16/`). All of it was done within the project by
the developer; none of it is replication by an unaffiliated party, and the AI review is not human peer review.
Independent replication is welcome — that is what this repository is for.

## Cite as

Houghtaling, N. ({YEAR}). *The D'Agapeyeff Cipher (1939): grille recovery and polyphonic-table identifiability under n-gram scoring.* {OWNER}. doi:{DOI}

## Copyright and licensing

© {YEAR} {OWNER}. The author, {AUTHOR}, carried out this work at {OWNER}, which holds the
copyright to the extent it owns the applicable rights. The report, its figures and the accompanying research materials
are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0), and the source code under
the Apache License 2.0. Copyright is asserted only in material eligible for protection under applicable law;
third-party materials keep their own rights and licenses, as set out in the repository's LICENSE and NOTICE files.
""")

    # ── line endings: LF for every text file we author; archived evidence kept byte for byte ──
    # Files whose SHA-256 is cited elsewhere (evidence/APPENDIX-C.md, lab/cipher/lm/CORPUS.md) keep their exact bytes,
    # CRLF included (the scripts as executed; Project Gutenberg's texts as distributed); .gitattributes marks them -text.
    PRESERVE = ["docs/FINDINGS.md", "lab/cipher/grille/grille_engine.py", "lab/cipher/grille/digraph_engine.py",
                "lab/cipher/round11/identifiability.py", "lab/cipher/lm/corpus/*.txt"]
    TEXT_EXT = {".md", ".py", ".txt", ".json", ".cff", ".csv", ".css", ".svg", ".sh", ".patch", ".sha256", ".yml",
                ".yaml", ".toml", ""}
    cited = (REPO / "evidence/APPENDIX-C.md").read_text(encoding="utf-8") + (REPO / "lab/cipher/lm/CORPUS.md").read_text(encoding="utf-8")
    preserved = {q for pat in PRESERVE for q in REPO.glob(pat)}
    normalized = []
    for q in sorted(REPO.rglob("*")):
        if not q.is_file() or q in preserved or q.suffix.lower() not in TEXT_EXT:
            continue
        b = q.read_bytes()
        if b"\r\n" in b:
            if sha(q)[:16] in cited:
                raise SystemExit(f"refusing to normalize {q.relative_to(REPO)}: its fingerprint is cited as evidence")
            q.write_bytes(b.replace(b"\r\n", b"\n"))
            normalized.append(q.relative_to(REPO).as_posix())
    write(".gitattributes", "\n".join([
        "# Text is stored and checked out with LF line endings, so a fresh clone matches MANIFEST.sha256 byte for byte.",
        "* text=auto eol=lf",
        *[f"*.{e} text eol=lf" for e in ("md", "py", "txt", "json", "cff", "csv", "css", "svg", "sh", "patch", "sha256",
                                         "yml", "yaml", "toml")],
        "COPYRIGHT text eol=lf", "LICENSE text eol=lf", "NOTICE text eol=lf",
        *[f"*.{e} binary" for e in ("pdf", "png", "jpg", "jpeg", "npy", "zip")],
        "# Archived evidence kept byte for byte (CRLF as executed / as distributed by Project Gutenberg); fingerprints are",
        "# cited in evidence/APPENDIX-C.md and lab/cipher/lm/CORPUS.md. Do not normalize.",
        *[f"{pat} -text" for pat in PRESERVE], ""]))
    print(f"normalized to LF: {len(normalized)} files; preserved byte for byte: {len(preserved)}")

    # ── manifest of everything ──
    files = sorted(p for p in REPO.rglob("*") if p.is_file() and p.name != "MANIFEST.sha256")
    (REPO / "MANIFEST.sha256").write_text("".join(f"{sha(p)}  {p.relative_to(REPO).as_posix()}\n" for p in files),
                                         encoding="utf-8")
    total = sum(p.stat().st_size for p in files)
    print(json.dumps({"repo": str(REPO), "files": len(files), "mb": round(total / 1e6, 1),
                      "appendix_rows": len(appendix), "fingerprint_only": sum(1 for a in appendix if a[2] is None),
                      "problems": problems}, indent=1))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
