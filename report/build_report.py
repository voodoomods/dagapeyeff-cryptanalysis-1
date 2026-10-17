"""Build the D'Agapeyeff report PDF: Markdown sections -> HTML (pandoc) -> PDF (Playwright Chromium).

Run in the agent container:  python /workspace/research/cipher/dagapeyeff/report/build_report.py [body.md]
Inputs (report/): front.md, the body (default body_final.md, else draft_body.md), back.md, figs/*.svg,
../evidence/MANIFEST.md. Output: report/DAgapeyeff-Report-VoodooMods.pdf (+ report.html for review).
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

R = Path("/workspace/research/cipher/dagapeyeff/report")
EV = R.parent / "evidence"
TITLE = "The D'Agapeyeff Cipher (1939)"
SUBTITLE = "Grille recovery and polyphonic-table identifiability under n-gram scoring"
AUTHOR = "Nicolas Houghtaling"
ORG = "VoodooMods LLC"
DATE = "October 17, 2026"
DOI = "10.5281/zenodo.23306263"
ORCID = "0009-0001-3192-544X"
import os

FINAL = os.environ.get("PEGASUS_FINAL") == "1"   # publication build: no draft / confidentiality marks

FIGS = {
    "fig1": ("fig1_cipher_grid", "The challenge cipher laid out 14 symbols per row. All eight occurrences of the five "
             "rare symbols fall in the last column; the other 13 columns use 13 symbols."),
    "fig2": ("fig2_flatness", "Left: the 13 message symbols occur almost equally often. Right: letters of English "
             "in a text of the same length, on the same scale. A one-to-one key keeps English's steep profile; the "
             "cipher does not have it."),
    "fig3": ("fig3_turning_grille", "How a turning grille scrambles a message, shown on a 4 × 4 card. Each turn "
             "exposes four new cells; after four turns every cell holds one letter and the grid is read row by row."),
    "fig4": ("fig4_ngram_order", "Practice ciphers: with the polyphonic table known, the grille is recovered (at least 45 of 49 orbits) on every practice "
             "cipher when candidate orders are scored by five- or six-symbol patterns; four-symbol scoring fails on "
             "four of six."),
    "fig5": ("fig5_tolerance", "The same search given a table with some letters in the wrong group. From six "
             "misplaced letters on, it never finds the grille."),
    "fig6": ("fig6_identifiability", "Truth-start test: how often the true table stays the best-scoring among its neighbors when the grille order is already "
             "known, by length of text, for two independent English models (100 practice ciphers each). At the "
             "cipher's 182 symbols it is about one in ten."),
}


def pandoc(md: str) -> str:
    return subprocess.run(["pandoc", "-f", "markdown+pipe_tables+smart", "-t", "html5", "--no-highlight"],
                          input=md, capture_output=True, text=True, check=True).stdout


def figure(key: str, n: int) -> str:
    name, cap = FIGS[key]
    svg = (R / "figs" / f"{name}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", svg)
    return (f'<figure id="{key}"><div class="svg">{svg}</div>'
            f'<figcaption><b>Figure {n}.</b> {html.escape(cap)}</figcaption></figure>')


def manifest_appendix() -> str:
    """Appendix C, written by release/build_release.py after verifying every fingerprint against the repository."""
    return (R / "APPENDIX-C.md").read_text(encoding="utf-8")


CODE = re.compile(r"(?<![A-Za-z0-9#-])([FRICO]\d{1,3})(?![0-9A-Za-z])")


def link_codes(html_body: str) -> str:
    """Make every case-file code in running text (F73, R29 ...) a link to its line in Appendix D.
    Text inside tags, <code>, existing links and the appendix's own anchors is left alone."""
    known = set(re.findall(r'id="code-([A-Z]\d+)"', html_body))
    out, depth_skip = [], 0
    for part in re.split(r"(<[^>]+>)", html_body):
        if part.startswith("<"):
            tag = part[1:].split()[0].rstrip(">").lower() if len(part) > 2 else ""
            if tag in ("code", "a", "pre"):
                depth_skip += 1
            elif tag in ("/code", "/a", "/pre"):
                depth_skip = max(0, depth_skip - 1)
            out.append(part)
        elif depth_skip:
            out.append(part)
        else:
            out.append(CODE.sub(lambda m: f'<a class="code" href="#code-{m.group(1)}">{m.group(1)}</a>'
                                if m.group(1) in known else m.group(1), part))
    return "".join(out)


def main():
    body_name = sys.argv[1] if len(sys.argv) > 1 else ("body_final.md" if (R / "body_final.md").exists() else "draft_body.md")
    parts = [(R / "front.md").read_text(encoding="utf-8"), (R / body_name).read_text(encoding="utf-8"),
             (R / "back.md").read_text(encoding="utf-8"), manifest_appendix(),
             (R / "codes.md").read_text(encoding="utf-8"), (R / "appendix-e.md").read_text(encoding="utf-8"),
             (R / "appendix-f.md").read_text(encoding="utf-8")]
    md = "\n\n".join(parts)
    if FINAL:   # drop draft-only passages
        md = re.sub(r"<!-- draft-only -->.*?<!-- /draft-only -->", "", md, flags=re.DOTALL)
    else:
        md = md.replace("<!-- draft-only -->", "").replace("<!-- /draft-only -->", "")
    md = re.sub(r"^#\s+[^#].*$", "", md, flags=re.MULTILINE)          # the cover carries the title; drop any H1
    seen = []

    def fig_sub(m):
        k = m.group(1)
        if k in seen:
            return ""
        seen.append(k)
        return f"\n\nFIGURE::{k}\n\n"
    md = re.sub(r"\{\{\s*(fig\d)\s*\}\}", fig_sub, md)
    body = pandoc(md)
    body = re.sub(r"<colgroup>.*?</colgroup>", "", body, flags=re.DOTALL)   # let the browser size columns by content
    for i, k in enumerate(seen, 1):
        body = re.sub(rf"<p>FIGURE::{k}</p>", figure(k, i), body)
        body = body.replace(f"[{k}]", f"Figure {i}")
    missing = [k for k in FIGS if k not in seen]
    body = link_codes(body)

    toc = []
    def anchor(m):
        title = " ".join(re.sub("<[^>]+>", "", m.group(2)).split())
        aid = "s" + str(len(toc))
        toc.append((title, aid))
        attrs = re.sub(r'\s*id="[^"]*"', "", m.group(1))
        return f'<h2 id="{aid}"{attrs}>{m.group(2)}</h2>'
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", anchor, body, flags=re.DOTALL)
    toc_html = "".join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for t, a in toc)

    css = (R / "report.css").read_text(encoding="utf-8")
    head = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(TITLE)}</title>
<style>{css}</style></head><body>"""
    cover = head + f"""
<section class="cover">
  <div class="cover-band"></div>
  <div class="cover-kicker">{"Research preprint" if FINAL else "Research preprint · Confidential pre-publication draft"}</div>
  <h1>{html.escape(TITLE)}</h1>
  <p class="cover-sub">{html.escape(SUBTITLE)}</p>
  <div class="cover-grid" aria-hidden="true">{''.join('<i></i>' for _ in range(14 * 6))}</div>
  <div class="cover-meta">
    <div><span>Author</span>{AUTHOR}, independent researcher<br><a href="https://orcid.org/{ORCID}">ORCID {ORCID}</a></div>
    <div><span>Affiliation</span>{ORG}</div>
    <div><span>Date</span>{DATE}</div>
    <div><span>DOI</span><a href="https://doi.org/{DOI}">doi:{DOI}</a></div>
  </div>
  <p class="cover-rights">© 2026 VoodooMods LLC. Report, figures and research materials: Creative Commons Attribution
  4.0 International License (CC BY 4.0). Source code: Apache License 2.0.</p>
</section></body></html>"""
    doc = head + f"""<section class="toc"><h2 class="toc-title">Contents</h2><ol>{toc_html}</ol></section>
<main>{body}</main>
</body></html>"""
    out_html = R / "report.html"
    out_html.write_text(doc, encoding="utf-8")
    cover_html = R / "cover.html"
    cover_html.write_text(cover, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    header = (f'<div style="font-family:Liberation Sans,Arial,sans-serif;font-size:7.5px;color:#7a7975;width:100%;'
              f'padding:0 0.75in;display:flex;justify-content:space-between">'
              f'<span>{html.escape(TITLE)} — {ORG}</span><span>{"doi:" + DOI if FINAL else "CONFIDENTIAL · PRE-PUBLICATION DRAFT"}</span></div>')
    footer = ('<div style="font-family:Liberation Sans,Arial,sans-serif;font-size:7.5px;color:#7a7975;width:100%;'
              'padding:0 0.75in;display:flex;justify-content:space-between">'
              f'<span>© 2026 {ORG} · CC BY 4.0 · {AUTHOR}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    pdf = R / "DAgapeyeff-Report-VoodooMods.pdf"
    cover_pdf, body_pdf = R / ".cover.pdf", R / ".body.pdf"
    margins = {"top": "0.85in", "bottom": "0.8in", "left": "0.75in", "right": "0.75in"}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(cover_html.as_uri(), wait_until="load")
        pg.pdf(path=str(cover_pdf), format="Letter", print_background=True, margin=margins)
        pg.goto(out_html.as_uri(), wait_until="load")
        pg.pdf(path=str(body_pdf), format="Letter", print_background=True, display_header_footer=True,
               header_template=header, footer_template=footer, margin=margins)
        b.close()
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for src in (cover_pdf, body_pdf):
        for pgx in PdfReader(str(src)).pages:
            w.add_page(pgx)
    rd = w
    w.add_metadata({"/Title": TITLE, "/Subject": SUBTITLE, "/Author": f"{AUTHOR} ({ORG}; ORCID {ORCID})",
                    "/Creator": "PegasusDMZ report builder", "/DOI": f"doi:{DOI}", "/Copyright": "(c) 2026 VoodooMods LLC. Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).", "/Keywords": "research preprint; D'Agapeyeff; turning grille; polyphonic; unicity distance"})
    with open(pdf, "wb") as fh:
        w.write(fh)
    print(json.dumps({"pdf": str(pdf), "pages": len(rd.pages), "figures": seen, "figures_missing": missing,
                      "sections": [t for t, _ in toc], "body": body_name}))


if __name__ == "__main__":
    main()
