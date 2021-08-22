# Unicode versions of the Byzantine text in `.csv` format

This folder contains Unicode versions of the `.CCT` files in the `textonly-beta-code` folder, which are the original files produced by Prof. Robinson. The `.csv` files in this folder are provided to you merely as a convenience. We have made efforts to make sure that these files faithfully represent the Beta-encoded `.CCT` files, but caution is advised since the conversion was made using an automated tool and its results have not been thoroughly checked by a human. Professor Robinson's `.CCT` files remain the ultimate source of truth.

The script used to convert the files from the Beta-encoded `.CCT` to the Unicode `.csv` is the `converter.py` file. You call it using `python3 converter.py` (or `python converter.py` depending on your particular settings.) It has been tested on Ubuntu 20.04 and Python 3.8. This script generates `.csv`s of all the books of the New Testament (including the Pericopa Adulterae, `PA.CCT`, and the verses from Acts 24, `ACT24.CCT`) and keeps two versions of each. The versions that include the textual variants are inside the `with-variants` folder, and the versions without textual variants are in the `no-variants` folder.

The script has dependencies, which are listed in the `requirements.txt` file. To install them, you can run `pip install -r requirements.txt`.
