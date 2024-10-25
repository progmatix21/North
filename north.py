#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# <North:north.py - trie based spelling suggester>
# Copyright (C) <2024>  <Atrij Talgery: github.com/progmatix21>
# SPDX-License-Identifier: AGPL-3.0-or-later
# https://www.gnu.org/licenses/agpl.txt
# https://spdx.org/licenses/AGPL-3.0-or-later.html
"""
from pytrie import SortedStringTrie as Trie
from difflib import SequenceMatcher
import functools
import timeit
import unittest

class North():
    '''
    Spelling suggester class
    '''

    chop = lambda s: s[:-1]  # class variable
    cache_size = 10
    
    def __init__(self,wordlist,cache_size=10):
        self._wordlist = wordlist
        self._ft = Trie()
        self._rt = Trie()
        North.cache_size = cache_size
        for i,k in enumerate(wordlist):
            self._ft[k] = i
            self._rt[k[::-1]] = i
            
    def _forward_check(self,msword:str) -> set:
        '''
        Input: mis-spelled word 
        Returns: spelling suggestions
        '''
        while(len(msword)>=1):
            if ss := list(self._ft.keys(prefix=msword)):
                return set(ss)
            else:
                msword = North.chop(msword)
                
        return set([])
    
    def _reverse_check(self,msword:str) -> set:
        '''
        Input: mis-spelled word 
        Returns: spelling suggestions
        '''
        rmsword = msword[::-1]
        while(len(rmsword)>=1):
            if ss := list(self._rt.keys(prefix=rmsword)):
                return set([w[::-1] for w in ss])
            else:
                rmsword = North.chop(rmsword)
                
        return set([])
    
    @functools.lru_cache(maxsize=10)
    def __call__(self,msword:str,topn:int=2) -> list:
        '''
        Return the combined output of the forward and reverse check.
        '''
        combined_set = self._forward_check(msword).union(self._reverse_check(msword))
        
        # Lambda function to calculate similarity
        similarity = lambda w1,w2: SequenceMatcher(None,w1,w2).ratio()
        
        # Sorted combined list of tuples keyed on similarity metric
        combined_tups = sorted([(similarity(msword,e),e) for e in combined_set],reverse=True)
        
        # Separate the words out, take the top two
        combined_list = list(zip(*combined_tups))[1][:min(topn,len(combined_tups))]
        
        
        if msword in combined_set:  # word is already correct
            return [msword]
        else:
            return combined_list



    

if __name__ == "__main__":
    
    wordlist = ["sugriva","sugreeva","sugar","superman","super","apple","human","hanuman"]
    misspelledwordlist = ["sgureeva","sugariva","sgurva","hanugreeva"]

    my_spelling_suggester = North(wordlist)
    print("Cache test")
    for msw in ["sgureeva"]*5:
        print(msw, timeit.timeit(lambda:my_spelling_suggester(msw)))
    
    class TestFunctions(unittest.TestCase):
        def setUp(self):
            pass
        
        # Check if correct word is in suggestions for the misspelled word.
        def test_forward_check(self):
            self.assertIn("sugreeva",my_spelling_suggester._forward_check("sgureeva"))
            
        def test_reverse_check(self):
            self.assertIn("sugreeva",my_spelling_suggester._reverse_check("sgureeva"))
            
    unittest.main()