## Appendix F. Language corpora and data provenance

Every external language source used in an experiment reported here, with where it came from, how it was processed and where it was used [F80]. Project Gutenberg texts were retrieved on October 11, 2026 from `https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt`; the text between Gutenberg's `*** START OF` and `*** END OF` markers was kept (the license header and footer removed) and nothing else changed. Catalog details below are quoted from each book's Project Gutenberg record (read October 16, 2026); every last-update date the records list predates the retrieval (two Latin records list none). SHA-256 fingerprints of the files used are in `lab/cipher/lm/CORPUS.md`. A source's role can differ between experiments: in particular the two Wells novels are part of model corpus A in Section 6.4 but are held out of every model, as plaintext, in Section 6.5.

**Table F.1. English novels (Project Gutenberg editions).**

| File | Work | Gutenberg | Record: released / last update | §6.4 corpus | §6.5 role | In repository |
|---|---|---|---|---|---|---|
| `adventures-holmes.txt` | *The Adventures of Sherlock Holmes*, Arthur Conan Doyle | [#1661](https://www.gutenberg.org/ebooks/1661) | Mar 1, 1999 / Oct 10, 2023 | A | model corpus A′ | yes |
| `great-expectations.txt` | *Great Expectations*, Charles Dickens (the text identifies itself as the 1867 edition) | [#1400](https://www.gutenberg.org/ebooks/1400) | Jul 1, 1998 / Dec 17, 2024 | B | model corpus B | yes |
| `hound-baskervilles.txt` | *The Hound of the Baskervilles*, Arthur Conan Doyle | [#2852](https://www.gutenberg.org/ebooks/2852) | Oct 1, 2001 / Aug 4, 2025 | A | model corpus A′ | yes |
| `man-who-was-thursday.txt` | *The Man Who Was Thursday: A Nightmare*, G. K. Chesterton | [#1695](https://www.gutenberg.org/ebooks/1695) | Apr 1, 1999 / Feb 5, 2024 | B | model corpus B | yes |
| `memoirs-holmes.txt` | *The Memoirs of Sherlock Holmes*, Arthur Conan Doyle | [#834](https://www.gutenberg.org/ebooks/834) | Mar 1, 1997 / Dec 2, 2023 | A | model corpus A′ | yes |
| `mysterious-affair-styles.txt` | *The Mysterious Affair at Styles*, Agatha Christie | [#863](https://www.gutenberg.org/ebooks/863) | Mar 1, 1997 / Apr 26, 2025 | B | model corpus B | no — public domain in the USA, in copyright in the UK and EU |
| `return-holmes.txt` | *The Return of Sherlock Holmes*, Arthur Conan Doyle | [#108](https://www.gutenberg.org/ebooks/108) | Mar 8, 2006 / Apr 25, 2026 | A | model corpus A′ | yes |
| `secret-adversary.txt` | *The Secret Adversary*, Agatha Christie | [#1155](https://www.gutenberg.org/ebooks/1155) | Jan 1, 1998 / Oct 29, 2022 | B | model corpus B | no — public domain in the USA, in copyright in the UK and EU |
| `secret-agent.txt` | *The Secret Agent: A Simple Tale*, Joseph Conrad (the text is the Methuen second edition (October 1907)) | [#974](https://www.gutenberg.org/ebooks/974) | Jul 1, 1997 / Feb 12, 2023 | A | model corpus A′ | yes |
| `tale-of-two-cities.txt` | *A Tale of Two Cities*, Charles Dickens | [#98](https://www.gutenberg.org/ebooks/98) | Jan 1, 1994 / Feb 26, 2026 | B | model corpus B | yes |
| `time-machine.txt` | *The Time Machine*, H. G. Wells | [#35](https://www.gutenberg.org/ebooks/35) | Oct 2, 2004 / Jun 16, 2026 | A | held-out plaintext (Wells prose) | yes |
| `war-and-peace.txt` | *War and Peace*, Leo Tolstoy, translated by Louise Maude and Aylmer Maude | [#2600](https://www.gutenberg.org/ebooks/2600) | Apr 1, 2001 / Jun 14, 2022 | B | model corpus B | yes |
| `war-of-the-worlds.txt` | *The War of the Worlds*, H. G. Wells | [#36](https://www.gutenberg.org/ebooks/36) | Oct 1, 2004 / Mar 30, 2026 | A | held-out plaintext (Wells prose) | yes |

Also requested on October 11 but never retrieved, because Gutenberg returned server errors: eBooks 558, 2097 and 1342. They are not in any corpus.

**Table F.2. Which text was used where.**

| Text | Size (letters) | Built from | Used in (this report) | Reproduce |
|---|---|---|---|---|
| Model text | 7,032,556 | all 13 novels, letters A–Z only, upper case, in file-name order | §4 example table (its first 2,000,000 letters: *Adventures*, *Great Expectations*, *Hound*, *The Man Who Was Thursday* and part of *Memoirs*); §6.1 [F78], §6.2 [F74], §6.3 [I47] | `tools/build_model_text.py` (needs the two Christie novels) |
| Corpus A / B | 2,360,321 / 4,672,235 | the 13 novels in file-name order, alternately (Table F.1) | §6.4 [F76] | `round11/identifiability.py` |
| Corpus A′ / B / A′ + B | 1,952,643 / 4,672,235 / 6,624,878 | A without the Wells novels; B; both | §6.5 [F77, F79] | `round12/review_checks.py`, `round12/comparability.py` |
| Wells prose | 407,678 | *The Time Machine* + *The War of the Worlds*, held out of every model in these experiments | §6.5 plaintexts and fresh passages [F77], §6.5 comparability [F79], §7 purpose-built four-square passages [O34] | as above; `round12/review_checks.py fsq` |
| Word sample | 60,000 | English words drawn by frequency from wordfreq (below); characters 130,000–190,000 of the stream | practice plaintexts of §6.1–6.4; word-sample setups of §6.5; §7 random-key four-square [R35]; [F71] | `lab/cipher/grille/plain_pool.txt` |
| Quadgram table | 26⁴ values | four-letter frequencies of the same wordfreq stream | [F71] (grille search with the letter key given) | `lab/cipher/grille/quad_en.npy` |
| English word stream | 200,000 per call | the same wordfreq sampling, generated on the fly | §2 flatness comparison [F31]; the book's sign system [R31] | PegasusDMZ agent tools (not in this repository) |
| Latin corpus | ≈ 2.7 M after filtering | the 10 Latin editions of Table F.3; lines that are mostly English removed | §2 Latin flatness comparison [F31, F80] | `lab/cipher/provenance/latin_flatness.py` (needs the agent tools) |

Plaintext and language model never come from the same text within an experiment: the word sample is drawn from wordfreq, not from the novels, and the Section 6.5 checks remove the Wells novels from every model before using them as plaintext.

**Table F.3. Latin editions (Project Gutenberg), used only for the Latin comparison of Section 2.** Not redistributed; fingerprints of the files used are in `lab/cipher/lm/CORPUS.md`.

| File | Work | Gutenberg | Record language | English apparatus |
|---|---|---|---|---|
| `augustine-confessiones.txt` | *Confessiones*, Augustine of Hippo; ed. Philippe Goibaud du Bois; E. B. Pusey | [#33849](https://www.gutenberg.org/ebooks/33849) | Latin | no |
| `caesar-bello-gallico.txt` | *C. Iuli Caesaris De Bello Gallico, I-IV*, Julius Caesar | [#218](https://www.gutenberg.org/ebooks/218) | Latin | no |
| `cicero-catilina.txt` | *Speeches against Catilina*, Marcus Tullius Cicero; ed. Ernest Alfred Upcott | [#39355](https://www.gutenberg.org/ebooks/39355) | English; Latin | yes — English notes or translation |
| `cicero-de-officiis.txt` | *De Officiis*, Marcus Tullius Cicero; Walter Miller (translator) | [#47001](https://www.gutenberg.org/ebooks/47001) | English | yes — English notes or translation |
| `cicero-orations.txt` | *Cicero's Orations*, Marcus Tullius Cicero | [#226](https://www.gutenberg.org/ebooks/226) | Latin | no |
| `descartes-meditationes.txt` | *Meditationes de prima philosophia*, René Descartes | [#23306](https://www.gutenberg.org/ebooks/23306) | Latin | no |
| `gellius.txt` | *Stories from Aulus Gellius: Being Selections and Adaptations from the Noctes Atticae*, Aulus Gellius; ed. G. Herbert Nall | [#25861](https://www.gutenberg.org/ebooks/25861) | Latin | yes — English notes or translation |
| `newton-principia.txt` | *Philosophiae Naturalis Principia Mathematica*, Isaac Newton | [#28233](https://www.gutenberg.org/ebooks/28233) | Latin | no |
| `virgil-aeneid.txt` | *Aeneidos*, Virgil | [#227](https://www.gutenberg.org/ebooks/227) | Latin | no |
| `viri-romae.txt` | *Selections from Viri Romae*, C. F. L'Homond; ed. Robert Arrowsmith; Charles Knapp | [#33311](https://www.gutenberg.org/ebooks/33311) | English; Latin | yes — English notes or translation |

The four editions with English apparatus are school editions or a facing translation; the Latin reader drops every line in which English function words make up 20% or more of the words, which leaves 0.5% English words in the stream. The Latin result of Section 2 depends on which editions are sampled: 345–374 of 1,000 windows for the full corpus, 167–182 for the six editions without English apparatus [F80].

**Word frequencies.** The word sample, the quadgram table and the English word stream come from the `wordfreq` package (Speer 2022; version 3.1.1 installed — regenerating the two shipped files with it reproduces them byte for byte): the 30,000 most frequent English words of its default list, sampled in proportion to frequency with a fixed seed (4321) and joined without spaces. wordfreq's English list combines Wikipedia, subtitles (OPUS OpenSubtitles 2018 and SUBTLEX: Brysbaert and New 2009; van Heuven et al. 2014), news, Google Books Ngrams, web text, Twitter and Reddit. Its code is under the Apache License 2.0 and its data files under CC BY-SA 4.0; the derived files in this repository are shared under CC BY-SA 4.0 accordingly (see `NOTICE`), not under the repository's CC BY 4.0.

**Rights.** Project Gutenberg's records state each book is public domain in the USA. The two Agatha Christie novels (author died 1976) remain in copyright in the UK and the EU, so they, and the model text built from them, are not redistributed. For the other English novels the authors and the War and Peace translators died before 1955; the Latin editions include editorial notes whose editors' dates are not all known. These notes are not legal advice; status outside the USA should be checked for any redistribution.
