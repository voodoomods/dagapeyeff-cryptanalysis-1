"""Rebuild lab/cipher/grille/model_text_big.txt from the 13 corpus novels (see lab/cipher/lm/CORPUS.md).

    python build_model_text.py lab/cipher/lm/corpus lab/cipher/grille/model_text_big.txt

The model text is the letters A-Z of the novels, upper-cased, in file-name order, nothing else. With the same corpus
files it reproduces the published SHA-256 exactly (checked by build_release.py).
"""
import glob
import os
import re
import sys


def build(corpus_dir: str) -> str:
    text = "".join(open(f, encoding="utf-8", errors="ignore").read()
                   for f in sorted(glob.glob(os.path.join(corpus_dir, "*.txt"))))
    return re.sub("[^A-Z]", "", text.upper())


if __name__ == "__main__":
    out = build(sys.argv[1])
    open(sys.argv[2], "w").write(out)
    print(f"{len(out):,} letters -> {sys.argv[2]}")
