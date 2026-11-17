# Unicode versions of the Byzantine text in `.csv` format

> **Curated editions:** the CSV files in this folder are the working-tree outputs for the current text. Per-edition CSV exports (official 2005, released 2005+2019, official 2018, released 2018+2023) live under [`editions/`](../editions) and are explained in [`docs/EDITIONS.md`](../docs/EDITIONS.md).

This folder contains Unicode versions of the original `.CCAT` and `.BP5` files produced by Prof. Robinson. The `.csv` files in this folder are provided to you merely as a convenience: they are generated from the authoritative machine-readable source in `source/`, while the published PDFs of the 2005 and 2018 editions are the ultimate source of truth for the printed text.

The scripts used to convert the files to the Unicode `.csv`s are in the `scripts` folder (see that folder's `README` for details).

## Words with more than one parsing

In the files inside the `strongs/with-parsing` folder, a word may be followed by two sets of Strong's number and parsing code. These are alternative parsings of the same word (for example, a neuter form that can be either nominative or accusative), not two separate words: based on the word's morphology, either parsing is applicable. The details of this convention are explained in the [`README` file inside the `source` folder](../source/README.md).
