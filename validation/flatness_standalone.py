"""Standalone F31 / F80 flatness test — no PegasusDMZ dependency (needs: python>=3.10, wordfreq==3.1.1, scipy).

A line-for-line port of the platform tool used for case F31 (flatness_tools.frequency_flatness with
compound_ciphers._lang_stream and cryptanalysis_tools._corpus_lines, PegasusDMZ commit 8c4e0fa): same text folding,
same English-line filter for the Latin corpus, same sampling, same seeds and the same order of random draws, so its
counts can be compared one for one with the published ones (lab/cipher/provenance/latin_flatness.json).

What it measures: the message (the 182 symbols outside column 14) uses 13 symbols with chi-square-vs-uniform p = the
cipher's value; for N random 182-letter windows of a language it counts windows whose letters are AT LEAST AS FLAT
  top:       through the 13 commonest letters alone
  balanced:  through the most even possible many-to-one table (a deliberately balanced grouping)   <- F31 / F80
  ordinary:  through ordinary merges (13 commonest kept, the rest scattered at random)
  pairs:     through random two-letters-per-symbol tables

    python flatness_standalone.py --lang en|la [--seed S] [--windows N] [--latin-dir DIR] [--latin-files a.txt,b.txt]

English: wordfreq's 30,000 most frequent English words, sampled by frequency (seed 4321), joined without spaces.
Latin:   the Project Gutenberg editions in --latin-dir (eBooks and fingerprints in lab/cipher/lm/CORPUS.md; download
         https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt and keep the text between the '*** START OF' and
         '*** END OF' lines), files in name order; every line in which English function words make up 20% or more of
         the words is dropped; the first 1,500,000 letters are skipped and the rest repeated to 200,000 letters.
"""
import argparse, heapq, json, random, re, unicodedata
from collections import Counter
from pathlib import Path

from scipy.stats import chisquare

A26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
HERE = Path(__file__).resolve().parent
EN_FUNCTION = set(
    "THE AND OF TO IN IS THAT IT WAS FOR WITH AS HIS ON BE AT BY THIS HAD NOT ARE BUT FROM OR HAVE AN THEY "
    "WHICH ONE YOU WERE HER ALL SHE THERE WOULD THEIR WE HIM BEEN HAS WHEN WHO WILL MORE NO IF OUT SO SAID "
    "WHAT UP ITS ABOUT INTO THAN THEM CAN ONLY OTHER NEW SOME COULD TIME THESE TWO MAY THEN DO FIRST ANY MY "
    "NOW SUCH LIKE OUR OVER MAN ME EVEN MOST MADE AFTER ALSO DID MANY BEFORE MUST THROUGH BACK YEARS WHERE "
    "MUCH YOUR WAY WELL DOWN SHOULD BECAUSE EACH JUST THOSE PEOPLE HOW TOO LITTLE STATE GOOD VERY MAKE "
    "WORLD STILL OWN SEE MEN WORK LONG GET HERE BETWEEN BOTH LIFE BEING UNDER NEVER DAY SAME ANOTHER KNOW "
    "NOTE NOTES EDITION CHAPTER PROJECT GUTENBERG EBOOK TRANSLATED TRANSLATION PAGE".split())


# English-style Cyrillic transliteration, applied (as in the platform) to any word containing Cyrillic letters.
# wordfreq 3.1.1's English top-30,000 list contains three such one-letter words (в, и, с -> V, I, S).
CYR_EN = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
          "й": "i", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
          "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
          "э": "e", "ю": "yu", "я": "ya", "і": "i", "ї": "i", "є": "ye", "ґ": "g", "ѣ": "e", "ѳ": "f", "ѵ": "i",
          "ў": "u", "ј": "j", "љ": "lj", "њ": "nj", "џ": "dzh", "ѓ": "g", "ќ": "k", "ѕ": "dz"}


def translit(text):
    out = []
    for ch in text or "":
        low = ch.lower()
        out.append((CYR_EN[low].upper() if ch != low else CYR_EN[low]) if low in CYR_EN else ch)
    return "".join(out)


def word_fold(word):
    return fold(translit(word) if any("Ѐ" <= ch <= "ӿ" for ch in word or "") else word)


def fold(text):
    t = unicodedata.normalize("NFKD", (text or "").replace("ß", "ss"))
    return "".join(c for c in t.upper() if "A" <= c <= "Z")


def message():
    """The 182 message symbols: the cipher's first 392 digits as 196 pairs, column 14 of the 14 x 14 grid removed."""
    d = "".join(ch for ch in (HERE.parent / "data" / "ciphertext.txt").read_text() if ch.isdigit())
    pairs = [d[i:i + 2] for i in range(0, 392, 2)]
    return [p for i, p in enumerate(pairs) if i % 14 != 13]


def english_stream(n=200000):
    from wordfreq import top_n_list, word_frequency
    keep = [(word_fold(w), word_frequency(w, "en")) for w in top_n_list("en", 30000)]
    keep = [(f, w) for f, w in keep if f]
    rnd = random.Random(4321)
    out, total = [], 0
    while total < n:
        w = rnd.choices([f for f, _ in keep], weights=[x for _, x in keep], k=2000)
        out += w
        total += sum(len(x) for x in w)
    return "".join(out)[:n]


def latin_stream(directory, files=None, n=200000):
    rows = []
    for f in sorted(Path(directory).glob("*.txt")):
        if files and f.name not in files:
            continue
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            ws = [w for w in (fold(x) for x in re.split(r"[^\w]+", line)) if w]
            if ws and sum(w in EN_FUNCTION for w in ws) / len(ws) < 0.2:
                rows.append(ws)
    text = "".join("".join(ws) for ws in rows)
    held = text[1_500_000:] or text
    return (held * (n // len(held) + 1))[:n], len(text)


def chi_p(counts, k=None):
    c = list(counts) + [0] * max(0, (k or len(counts)) - len(counts))
    return float(chisquare(c).pvalue) if sum(c) else 1.0


def balanced_merge(counts, k):
    h = [(0, i) for i in range(k)]
    for c in sorted(counts, reverse=True):
        s, i = heapq.heappop(h)
        heapq.heappush(h, (s + c, i))
    return [s for s, _ in h]


def flatness(stream, windows, rnd, msg):
    c = Counter(msg)
    k, n = len(c), len(msg)
    real = chi_p(list(c.values()))
    top = best = ordinary = pairs = 0
    letters = []
    for _ in range(max(100, min(int(windows), 5000))):
        o = rnd.randrange(0, len(stream) - n - 1)
        w = Counter(stream[o:o + n])
        vals = sorted(w.values(), reverse=True)
        letters.append(len(vals))
        top += chi_p(vals[:k], k) >= real
        best += chi_p(balanced_merge(vals, k)) >= real
        bins = [0] * k
        for j, v in enumerate(vals):
            bins[j if j < k else rnd.randrange(k)] += v
        ordinary += chi_p(bins) >= real
        L = list(A26)
        rnd.shuffle(L)
        table = {ch: i % k for i, ch in enumerate(L)}
        pc = Counter(table[ch] for ch in stream[o:o + n] if ch in table)
        pairs += chi_p(list(pc.values()), k) >= real
    m = len(letters)
    return {"symbols": n, "distinct": k, "cipher_chi_square_p": round(real, 3),
            "median_distinct_letters": sorted(letters)[m // 2], "min_distinct_letters": min(letters),
            "max_distinct_letters": max(letters), "windows": m,
            "as_flat_top_letters": f"{top}/{m}", "as_flat_best_balanced_table": f"{best}/{m}",
            "as_flat_ordinary_merges": f"{ordinary}/{m}", "as_flat_two_letter_cells": f"{pairs}/{m}"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["en", "la"], required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--windows", type=int, default=1000)
    ap.add_argument("--latin-dir", default=str(HERE.parent / "lab" / "cipher" / "lang" / "la"))
    ap.add_argument("--latin-files", default="")
    a = ap.parse_args()
    if a.lang == "en":
        s, size = english_stream(), None
    else:
        s, size = latin_stream(a.latin_dir, set(a.latin_files.split(",")) if a.latin_files else None)
    r = flatness(s, a.windows, random.Random(a.seed), message())
    r.update(lang=a.lang, seed=a.seed, latin_letters_after_filter=size,
             latin_files=a.latin_files or ("all" if a.lang == "la" else None))
    print(json.dumps(r))
