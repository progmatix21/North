#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# <Product:filename - Description>
# Copyright (C) <202x>  <Atrij Talgery: github.com/progmatix21>
# SPDX-License-Identifier: AGPL-3.0-or-later
# https://www.gnu.org/licenses/agpl.txt
# https://spdx.org/licenses/AGPL-3.0-or-later.html
"""
import timeit
import time
from north import North

# Use the linux dictionary file
dictfile = "/usr/share/dict/american-english"

with open(dictfile,"r") as f:
    allwords = f.readlines()
    
clean_words = [w.strip("\n") for w in allwords if "'" not in w]
clean_words.extend(["North Pole","United States of America"])

# time the trie building step
start = time.time()
my_spelling_suggester = North(clean_words)
end = time.time()

print(f"Initialized {len(clean_words)} spellings in {end-start} seconds.")

misspelled_word_list = ["dgo","cta","kat","onoin","crraot",
    "pple","appl","og","carro","arroot","hosre","ohrse","aplpe",
    "Unted Stts of Amrica","Porth Nole"]

for word in misspelled_word_list:
    print(word, my_spelling_suggester(word, topn=5))

