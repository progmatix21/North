#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# <North: example_north.py- an example to run North>
# Copyright (C) <2024>  <Atrij Talgery: github.com/progmatix21>
# SPDX-License-Identifier: AGPL-3.0-or-later
# https://www.gnu.org/licenses/agpl.txt
# https://spdx.org/licenses/AGPL-3.0-or-later.html
"""

from north import North

correct_word_list = ["Hayagreeva","Rama","Red","Violet","Blue","Green","Hanuman","Sugreeva",
                     "Bangalore","Bengaluru","India","Indianapolis","New Delhi"]

misspelled_word_list = ["Hanugreeva","hanman","Indiia","Bengalure","New Deli","Viola","Bloo"]

my_spelling_suggester = North(correct_word_list)

for misspelled_word in misspelled_word_list:
    print(misspelled_word, my_spelling_suggester(misspelled_word,topn=2))