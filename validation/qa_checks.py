"""Publication-integrity checks on a built release (repository folder + PDF). Read-only.

    python validation/qa_checks.py REPO_DIR [--out qa.json]

Each check prints PASS / FAIL / WARN with what it found. Needs pypdf for the PDF checks (skipped with a WARN without it).
"""
import argparse, hashlib, json, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("--out")
a = ap.parse_args()
R = Path(a.repo)
out = []


def rec(name, ok, detail, warn=False):
    st = "PASS" if ok else ("WARN" if warn else "FAIL")
    out.append({"check": name, "status": st, "detail": detail})
    print(f"{st:5} {name}: {detail if isinstance(detail, str) else json.dumps(detail)[:300]}")


# 1. manifest
lines = (R / "MANIFEST.sha256").read_text().splitlines()
bad = [l.split("  ", 1)[1] for l in lines if hashlib.sha256((R / l.split("  ", 1)[1]).read_bytes()).hexdigest() != l.split("  ", 1)[0]]
listed = {l.split("  ", 1)[1] for l in lines}
unlisted = [p.relative_to(R).as_posix() for p in R.rglob("*") if p.is_file() and ".git" not in p.parts
            and p.name != "MANIFEST.sha256" and p.relative_to(R).as_posix() not in listed]
rec("manifest", not bad and not unlisted, {"files": len(lines), "mismatch": bad, "unlisted": unlisted})

# 2. text of every shipped text file + the PDF
TEXT_EXT = {".md", ".py", ".sh", ".txt", ".cff", ".json", ".patch", ""}
texts = {}
for p in R.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.suffix in TEXT_EXT and p.stat().st_size < 5_000_000:
        try:
            texts[p.relative_to(R).as_posix()] = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass
pdfs = sorted(R.rglob("*.pdf"))
own_pdf = [p for p in pdfs if "literature" not in p.parts]
try:
    from pypdf import PdfReader
    for p in own_pdf:
        rd = PdfReader(str(p))
        texts[p.relative_to(R).as_posix()] = "\n".join(pg.extract_text() or "" for pg in rd.pages)
        m = rd.metadata or {}
        rec(f"pdf {p.name}", len(rd.pages) > 0, {"pages": len(rd.pages), "title": m.get("/Title"), "author": m.get("/Author"),
                                                  "creation": str(m.get("/CreationDate"))[:10]})
except ImportError:
    rec("pdf", False, "pypdf not installed - PDF checks skipped", warn=True)

OWN = {k: v for k, v in texts.items() if not k.startswith(("docs/literature/", "docs/FINDINGS.md", "lab/cipher/lm/corpus/",
                                                            "evidence/", "lab/cipher/round", "lab/cipher/grille/",
                                                            "docs/audit-2026-10-15/proposed.patch", "docs/validation-2026-10-16/logs/",
                                                            "docs/validation-2026-10-16/rerun/", "docs/validation-2026-10-16/f6",
                                                            "docs/validation-2026-10-16/flatness/", "LICENSE", "docs/BRIEFING"))}


def grep(pattern, where=OWN, flags=re.I):
    rx = re.compile(pattern, flags)
    hits = []
    for k, v in where.items():
        for i, line in enumerate(v.splitlines(), 1):
            if rx.search(line):
                hits.append(f"{k}:{i}: {line.strip()[:140]}")
    return hits


report_pdf = {k: v for k, v in texts.items() if k.endswith(".pdf")}
# Documents a reader sees (Markdown, PDF, citation file); code and the fact-check log (a record of past wording) excluded.
DOCS = {k: v for k, v in OWN.items() if k.endswith((".md", ".pdf", ".cff")) and not k.endswith("FACTCHECK-LOG.md")}
rec("no pre-publication label", not grep(r"pre-publication|not for distribution", DOCS), grep(r"pre-publication|not for distribution", DOCS)[:5])
rec("not labeled revised", not grep(r"\(revised\)|revised edition", report_pdf), grep(r"\(revised\)|revised edition", report_pdf)[:5])
arr = [h for h in grep(r"all rights reserved", DOCS) if not re.search(r"author|hendrick|zenodo\.23241303", h, re.I)]
rec("no 'All Rights Reserved' on own material", not arr, arr[:5])
rec("reviewer attribution", not grep(r"GPT-6|\bSol\b", DOCS, 0), grep(r"GPT-6|\bSol\b", DOCS, 0)[:5])
cover = {k: v[:3000] for k, v in report_pdf.items() if "Report" in k}
rec("preprint label on cover", bool(grep(r"research preprint", cover)), "found on the cover page" if grep(r"research preprint", cover) else "missing")
rec("publication-status statement", bool(grep(r"not been formally peer-reviewed", {**report_pdf, "README.md": texts.get("README.md", "")})), "present")
# a line mentioning peer review must carry a negation (statements continue across wrapped lines, so check the pair)
peer = []
for k, v in DOCS.items():
    ls = v.splitlines()
    for i, line in enumerate(ls):
        if re.search(r"peer[- ]?review", line, re.I) and not re.search(r"\bnot\b|\bno\b|\bnor\b|without|isn't",
                                                                      " ".join(ls[max(0, i - 1):i + 1]), re.I):
            peer.append(f"{k}:{i + 1}: {line.strip()[:140]}")
rec("no claim of external peer review", not peer, peer[:8], warn=bool(peer))
tod = grep(r"\b([01]?\d|2[0-3]):[0-5]\d\b(?!:)", DOCS, 0)
tod = [h for h in tod if not re.search(r"\d+:\d+:\d+|ratio|1:\d{2,}|https?://", h)]
rec("no times of day in documents", not tod, tod[:8], warn=bool(tod))
UK = (r"\b(organisations?|organised?|programmes?|colours?|behaviours?|analysed|analysing|catalogues?|catalogued|"
      r"licences?|favours?|centres?|modelling|labelled|travelled|judgements?)\b")
uk = grep(UK, DOCS)
rec("American English spellings", not uk, uk[:10], warn=bool(uk))
readme = texts.get("README.md", "")
rec("DOI marked reserved", "DOI (reserved)" in readme, "README says reserved" if "DOI (reserved)" in readme else "README presents DOI as live")
rec("license exceptions listed", "License exceptions" in readme and "CC BY-SA 4.0" in readme, "README section present")
cff = texts.get("CITATION.cff", "")
rec("CITATION.cff", 'date-released: "2026-10-17"' in cff and "status: preprint" in cff,
    {"date-released": re.findall(r"date-released: \S+", cff), "status": re.findall(r"status: \S+", cff)})
local = grep(r"C:\\\\Users|C:/Users|/c/Users|OneDrive", {k: v for k, v in OWN.items() if not k.endswith(".pdf")}, 0)
rec("no local machine paths", not local, local[:8], warn=bool(local))
codes = set(re.findall(r'id="code-([A-Z]\d+)"', texts.get("report/codes.md", "")))
body = texts.get("report/body_final.md", "") + texts.get("report/back.md", "")
cited = set(re.findall(r"\b([FROICS]\d{1,3})\b", " ".join(re.findall(r"\[([A-Z0-9, ]+)\]", body))))
rec("every cited case code defined", cited <= codes, sorted(cited - codes))
rec("letter-range correction (F81)", "17 to 22" not in texts.get("report/body_final.md", ""), "old range removed")
if a.out:
    Path(a.out).write_text(json.dumps({"date": "2026-10-16", "checks": out}, indent=1))
print({s: sum(c["status"] == s for c in out) for s in ("PASS", "WARN", "FAIL")})
