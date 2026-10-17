# Language corpora

Provenance of every external language text used in the study; the report's Appendix F has the same record with each text's role per experiment. Source of truth: `docs/sources.json`.

## English novels (13)

Retrieved 2026-10-11 from `https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt`; processing: kept the text between the '*** START OF THE/THIS PROJECT GUTENBERG ...' and '*** END OF THE/THIS PROJECT GUTENBERG' markers (license header and footer removed); otherwise unchanged, original CRLF line endings kept. Catalog details are quoted from each book's Project Gutenberg record (read 2026-10-16). 'First published' is a standard reference date, not taken from the files. The English language models are built from these novels; `tools/build_model_text.py` rebuilds `lab/cipher/grille/model_text_big.txt` from them and, with these exact files, reproduces the fingerprint below.

| File | Work | Gutenberg eBook | Record: released / last update | First published | In this repository | SHA-256 |
|---|---|---|---|---|---|---|
| `adventures-holmes.txt` | *The Adventures of Sherlock Holmes*, Arthur Conan Doyle | [1661](https://www.gutenberg.org/ebooks/1661) | Mar 1, 1999 / Oct 10, 2023 | 1892 | yes - public domain in the USA | `6ab87b6e06ff6617c2b5d235af1f62395097ad1ac0cc360655d2807fdb5ed2e9` |
| `great-expectations.txt` | *Great Expectations*, Charles Dickens | [1400](https://www.gutenberg.org/ebooks/1400) | Jul 1, 1998 / Dec 17, 2024 | 1861 | yes - public domain in the USA | `e17a38e1e0f59d8f672ff0a1542480464aa4f7e7de423e3c6af73d707c37a636` |
| `hound-baskervilles.txt` | *The Hound of the Baskervilles*, Arthur Conan Doyle | [2852](https://www.gutenberg.org/ebooks/2852) | Oct 1, 2001 / Aug 4, 2025 | 1902 | yes - public domain in the USA | `0c29343b1251ea960511f5c15c90701f324a7cd4cbaaa0f6be1ef07999d06bfa` |
| `man-who-was-thursday.txt` | *The Man Who Was Thursday: A Nightmare*, G. K. Chesterton | [1695](https://www.gutenberg.org/ebooks/1695) | Apr 1, 1999 / Feb 5, 2024 | 1908 | yes - public domain in the USA | `458ce588f6d7453066184c427cc64b2df48454fc2f7be129818c0b96e9f573c6` |
| `memoirs-holmes.txt` | *The Memoirs of Sherlock Holmes*, Arthur Conan Doyle | [834](https://www.gutenberg.org/ebooks/834) | Mar 1, 1997 / Dec 2, 2023 | 1894 | yes - public domain in the USA | `8fdc18addff2b672df75d8bc93519a7c697db970429b255bad07e21198db982e` |
| `mysterious-affair-styles.txt` | *The Mysterious Affair at Styles*, Agatha Christie | [863](https://www.gutenberg.org/ebooks/863) | Mar 1, 1997 / Apr 26, 2025 | 1920 | not redistributed - public domain in the USA, still in copyright in the UK and EU (author d. 1976); obtain from Project Gutenberg | `9ed963de1ca76825aa28b3d286d84d2629695cbd0508554ef105af8959dc0743` |
| `return-holmes.txt` | *The Return of Sherlock Holmes*, Arthur Conan Doyle | [108](https://www.gutenberg.org/ebooks/108) | Mar 8, 2006 / Apr 25, 2026 | 1905 | yes - public domain in the USA | `678f4ccaa81c9ad4992dd569ea5f15e66f03a68e528522ba9e09322b190d55ef` |
| `secret-adversary.txt` | *The Secret Adversary*, Agatha Christie | [1155](https://www.gutenberg.org/ebooks/1155) | Jan 1, 1998 / Oct 29, 2022 | 1922 | not redistributed - public domain in the USA, still in copyright in the UK and EU (author d. 1976); obtain from Project Gutenberg | `f8221d52f1e31b6d9e78d412e4d148c13af974db0025708fd136b51c05e02900` |
| `secret-agent.txt` | *The Secret Agent: A Simple Tale*, Joseph Conrad | [974](https://www.gutenberg.org/ebooks/974) | Jul 1, 1997 / Feb 12, 2023 | 1907 | yes - public domain in the USA | `c690f1d04e47f48e28366f413706b601f7cba1857db6d312562e0234bcb8ad2d` |
| `tale-of-two-cities.txt` | *A Tale of Two Cities*, Charles Dickens | [98](https://www.gutenberg.org/ebooks/98) | Jan 1, 1994 / Feb 26, 2026 | 1859 | yes - public domain in the USA | `fd3bb9a03debee76ed2fc0c62bd0f1db1c65eeb6fc3e5282e6bdb01b864d1f3b` |
| `time-machine.txt` | *The Time Machine*, H. G. Wells | [35](https://www.gutenberg.org/ebooks/35) | Oct 2, 2004 / Jun 16, 2026 | 1895 | yes - public domain in the USA | `5653945db706fe132c6507df5f2937fb70b14e0d8bd973b95ca3f457f2d6ddd2` |
| `war-and-peace.txt` | *War and Peace*, Leo Tolstoy, translated by Louise Maude and Aylmer Maude | [2600](https://www.gutenberg.org/ebooks/2600) | Apr 1, 2001 / Jun 14, 2022 | 1869 | yes - public domain in the USA | `a5cc99893d57434df2cebf9be20762da4767f6c2963dd4b57a68608f99535566` |
| `war-of-the-worlds.txt` | *The War of the Worlds*, H. G. Wells | [36](https://www.gutenberg.org/ebooks/36) | Oct 1, 2004 / Mar 30, 2026 | 1898 | yes - public domain in the USA | `706f656f4ef2df8705d84d6cca20d4f5ff442102a8cc7adaf64ac318d80abf87` |

Also requested on 2026-10-11 but never retrieved (Gutenberg returned HTTP 503/504): eBooks 558 (The Thirty-Nine Steps), 2097 (The Sign of the Four), 1342 (Pride and Prejudice). They are not in the corpus.

## Latin editions (10) - not redistributed

Used only for the Latin comparison of case F31 / F80 (report Section 2). Same retrieval and processing as above; the Latin reader then drops lines that are mostly English. Obtain from Project Gutenberg.

| File | Work | Gutenberg eBook | Record language | English apparatus | SHA-256 |
|---|---|---|---|---|---|
| `augustine-confessiones.txt` | *Confessiones*, Augustine of Hippo (ed. Philippe Goibaud du Bois; E. B. Pusey) | [33849](https://www.gutenberg.org/ebooks/33849) | Latin | no | `2c1f0d680359ac5fa07b333183af45fc6cbf6c5ff9e8ecef17076a0baab7514b` |
| `caesar-bello-gallico.txt` | *C. Iuli Caesaris De Bello Gallico, I-IV*, Julius Caesar | [218](https://www.gutenberg.org/ebooks/218) | Latin | no | `a1a46119b3fd9c387a12484534255b7734be7a66f15b89cfc2a0f84b6071f301` |
| `cicero-catilina.txt` | *Speeches against Catilina*, Marcus Tullius Cicero (ed. Ernest Alfred Upcott) | [39355](https://www.gutenberg.org/ebooks/39355) | English; Latin | yes | `4ecb402900c118dbc5577422d4ff3d60d536ca56ca1a8e19a04fa07ed103bb73` |
| `cicero-de-officiis.txt` | *De Officiis*, Marcus Tullius Cicero (Walter Miller (translator)) | [47001](https://www.gutenberg.org/ebooks/47001) | English | yes | `ef2802f9093c0733f043df1a1425eeee4ec3ad6aeeaf22feb55dc7a0c222b8e7` |
| `cicero-orations.txt` | *Cicero's Orations*, Marcus Tullius Cicero | [226](https://www.gutenberg.org/ebooks/226) | Latin | no | `aa5707be9c6d3f0787a491007365d9f75bd1f5c5b9d69d8e5d42b3c086bd6206` |
| `descartes-meditationes.txt` | *Meditationes de prima philosophia*, René Descartes | [23306](https://www.gutenberg.org/ebooks/23306) | Latin | no | `995418a65651c956b03d2cde83053b108af2e3180cc79fb743dd6f33fc04af24` |
| `gellius.txt` | *Stories from Aulus Gellius: Being Selections and Adaptations from the Noctes Atticae*, Aulus Gellius (ed. G. Herbert Nall) | [25861](https://www.gutenberg.org/ebooks/25861) | Latin | yes | `c08934263318cf22cd0b5565dd1951e3a760ad6737bf3a541b2896cc5fd2793e` |
| `newton-principia.txt` | *Philosophiae Naturalis Principia Mathematica*, Isaac Newton | [28233](https://www.gutenberg.org/ebooks/28233) | Latin | no | `db8a65085360468e0c053cc9329e25189eb7226acf4ee6d5fb050b2d15b9280f` |
| `virgil-aeneid.txt` | *Aeneidos*, Virgil | [227](https://www.gutenberg.org/ebooks/227) | Latin | no | `f75de7822051042020e553eb92d469a73002490f7aac0fea67a72125eca02ea2` |
| `viri-romae.txt` | *Selections from Viri Romae*, C. F. L'Homond (ed. Robert Arrowsmith; Charles Knapp) | [33311](https://www.gutenberg.org/ebooks/33311) | English; Latin | yes | `9148149fb0c006a67164096b73aca1c3642c2656b5edd9eb69b82cd0dcbee2e3` |

## Word frequencies (wordfreq)

`plain_pool.txt`, `quad_en.npy` and the practice plaintexts quoted in `bench-2.json` are derived from wordfreq 3.1.1 (installed; regenerating the shipped derived files with it reproduces them byte for byte): English, top 30,000 words of wordfreq's default 'best' list; per the wordfreq README, English combines seven source types: Wikipedia, subtitles (OPUS OpenSubtitles 2018 and SUBTLEX), news (NewsCrawl 2014, GlobalVoices), books (Google Books Ngrams 2012), web text (OSCAR), Twitter and Reddit. Code license Apache-2.0; data license CC BY-SA 4.0 (per the wordfreq README). Cite: Speer, R. (2022). rspeer/wordfreq: v3.0 (v3.0.2). Zenodo. doi:10.5281/zenodo.7199437. Attribution terms: SUBTLEX data: derived work must credit the SUBTLEX authors and keep it clear that SUBTLEX is freely available data; Google Books Ngram Viewer: acknowledgement and a link to http://books.google.com/ngrams appreciated; OpenSubtitles: attribution.


`lab/cipher/grille/model_text_big.txt` (not redistributed - it contains the text of every novel above): SHA-256 `4db3e3d6f7c0dbf0f6496b8f7e58afb3b8a8088ef905063078c3447cc6c24a48`. Rebuild: `python tools/build_model_text.py lab/cipher/lm/corpus lab/cipher/grille/model_text_big.txt`.
