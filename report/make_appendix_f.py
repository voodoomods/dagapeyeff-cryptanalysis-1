"""Write appendix-f.md — Language corpora and data provenance — from release/sources.json (the verified record).

    python make_appendix_f.py        (stdlib only; reads release/sources.json, or docs/sources.json in the repository)
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
SRC = next(q for q in (R.parent / "release" / "sources.json", R.parent / "docs" / "sources.json") if q.exists())
S = json.loads(SRC.read_text(encoding="utf-8"))   # working tree: release/; published repository: docs/
EN, LA, WF, RET = S["english"], S["latin"], S["wordfreq"], S["retrieval"]
WELLS = {"time-machine.txt", "war-of-the-worlds.txt"}
CHRISTIE = {"mysterious-affair-styles.txt", "secret-adversary.txt"}


def gb(i):
    return f"[#{i}](https://www.gutenberg.org/ebooks/{i})"


out = ["## Appendix F. Language corpora and data provenance", "",
       "Every external language source used in an experiment reported here, with where it came from, how it was "
       "processed and where it was used [F80]. Project Gutenberg texts were retrieved on October 11, 2026 from "
       f"`{RET['url_pattern']}`; the text between Gutenberg's `*** START OF` and `*** END OF` markers was kept (the "
       "license header and footer removed) and nothing else changed. Catalog details below are quoted from each "
       "book's Project Gutenberg record (read October 16, 2026); every last-update date the records list predates the "
       "retrieval (two Latin records list none). "
       "SHA-256 fingerprints of the files used are in `lab/cipher/lm/CORPUS.md`. A source's role can differ between "
       "experiments: in particular the two Wells novels are part of model corpus A in Section 6.4 but are held out of "
       "every model, as plaintext, in Section 6.5.", "",
       "**Table F.1. English novels (Project Gutenberg editions).**", "",
       "| File | Work | Gutenberg | Record: released / last update | §6.4 corpus | §6.5 role | In repository |",
       "|---|---|---|---|---|---|---|"]
for e in EN:
    who = e["author"] + (f", translated by {e['translator']}" if e["translator"] else "")
    role65 = ("held-out plaintext (Wells prose)" if e["file"] in WELLS else f"model corpus {'A′' if e['half'] == 'A' else 'B'}")
    repo = "no — public domain in the USA, in copyright in the UK and EU" if e["file"] in CHRISTIE else "yes"
    note = f" ({e['note']})" if e.get("note") and "translator credit" not in e["note"] else ""
    out.append(f"| `{e['file']}` | *{e['title']}*, {who}{note} | {gb(e['id'])} | {e['release']} / {e['last_update']} | "
               f"{e['half']} | {role65} | {repo} |")
out += ["", "Also requested on October 11 but never retrieved, because Gutenberg returned server errors: eBooks 558, "
        "2097 and 1342. They are not in any corpus.", "",
        "**Table F.2. Which text was used where.**", "",
        "| Text | Size (letters) | Built from | Used in (this report) | Reproduce |", "|---|---|---|---|---|",
        "| Model text | 7,032,556 | all 13 novels, letters A–Z only, upper case, in file-name order | §4 example table (its first 2,000,000 letters: *Adventures*, *Great Expectations*, *Hound*, *The Man Who Was Thursday* and part of *Memoirs*); §6.1 [F78], §6.2 [F74], §6.3 [I47] | `tools/build_model_text.py` (needs the two Christie novels) |",
        "| Corpus A / B | 2,360,321 / 4,672,235 | the 13 novels in file-name order, alternately (Table F.1) | §6.4 [F76] | `round11/identifiability.py` |",
        "| Corpus A′ / B / A′ + B | 1,952,643 / 4,672,235 / 6,624,878 | A without the Wells novels; B; both | §6.5 [F77, F79] | `round12/review_checks.py`, `round12/comparability.py` |",
        "| Wells prose | 407,678 | *The Time Machine* + *The War of the Worlds*, held out of every model in these experiments | §6.5 plaintexts and fresh passages [F77], §6.5 comparability [F79], §7 purpose-built four-square passages [O34] | as above; `round12/review_checks.py fsq` |",
        "| Word sample | 60,000 | English words drawn by frequency from wordfreq (below); characters 130,000–190,000 of the stream | practice plaintexts of §6.1–6.4; word-sample setups of §6.5; §7 random-key four-square [R35]; [F71] | `lab/cipher/grille/plain_pool.txt` |",
        "| Quadgram table | 26⁴ values | four-letter frequencies of the same wordfreq stream | [F71] (grille search with the letter key given) | `lab/cipher/grille/quad_en.npy` |",
        "| English word stream | 200,000 per call | the same wordfreq sampling, generated on the fly | §2 flatness comparison [F31]; the book's sign system [R31] | PegasusDMZ agent tools (not in this repository) |",
        "| Latin corpus | ≈ 2.7 M after filtering | the 10 Latin editions of Table F.3; lines that are mostly English removed | §2 Latin flatness comparison [F31, F80] | `lab/cipher/provenance/latin_flatness.py` (needs the agent tools) |",
        "",
        "Plaintext and language model never come from the same text within an experiment: the word sample is drawn from "
        "wordfreq, not from the novels, and the Section 6.5 checks remove the Wells novels from every model before using "
        "them as plaintext.", "",
        "**Table F.3. Latin editions (Project Gutenberg), used only for the Latin comparison of Section 2.** Not "
        "redistributed; fingerprints of the files used are in `lab/cipher/lm/CORPUS.md`.", "",
        "| File | Work | Gutenberg | Record language | English apparatus |", "|---|---|---|---|---|"]
for e in LA:
    ed = f"; ed. {e['editor']}" if e["editor"] and "translator" not in e["editor"] else (f"; {e['editor']}" if e["editor"] else "")
    out.append(f"| `{e['file']}` | *{e['title']}*, {e['author']}{ed} | {gb(e['id'])} | {e['record_language']} | "
               f"{'yes — English notes or translation' if e['english_apparatus'] else 'no'} |")
out += ["",
        "The four editions with English apparatus are school editions or a facing translation; the Latin reader drops "
        "every line in which English function words make up 20% or more of the words, which leaves 0.5% English words in "
        "the stream. The Latin result of Section 2 depends on which editions are sampled: 345–374 of 1,000 windows for "
        "the full corpus, 167–182 for the six editions without English apparatus [F80].", "",
        "**Word frequencies.** The word sample, the quadgram table and the English word stream come from the "
        f"`wordfreq` package (Speer 2022; version {WF['version'].split(' ')[0]} installed — regenerating the two shipped "
        "files with it reproduces them byte for byte): the 30,000 most frequent English words of its default list, "
        "sampled in proportion to frequency with a fixed seed (4321) and joined without spaces. wordfreq's English list "
        "combines Wikipedia, subtitles (OPUS OpenSubtitles 2018 and SUBTLEX: Brysbaert and New 2009; van Heuven et al. "
        "2014), news, Google Books Ngrams, web text, Twitter and Reddit. Its code is under the Apache License 2.0 and "
        "its data files under CC BY-SA 4.0; the derived files in this repository are shared under CC BY-SA 4.0 "
        "accordingly (see `NOTICE`), not under the repository's CC BY 4.0.", "",
        "**Rights.** Project Gutenberg's records state each book is public domain in the USA. The two Agatha Christie "
        "novels (author died 1976) remain in copyright in the UK and the EU, so they, and the model text built from "
        "them, are not redistributed. For the other English novels the authors and the War and Peace translators died "
        "before 1955; the Latin editions include editorial notes whose editors' dates are not all known. These notes "
        "are not legal advice; status outside the USA should be checked for any redistribution.", ""]
(R / "appendix-f.md").write_text("\n".join(out), encoding="utf-8")
print("appendix-f.md:", len(out), "lines")
