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
from fastDamerauLevenshtein import damerauLevenshtein
import functools
import timeit
import unittest

class North():
    '''
    Spelling suggester class
    '''

    chop = lambda s: s[:-1]  # class variable
    cache_size = 10
    tailswap = lambda s: s[:-2]+s[-1]+s[-2] if len(s) >= 2 else s

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
        Assumes end of msword is mangled.
        
        Works as follows:
        Start with misspelled word and check all possible completion keys.
        e.g. the word 'appl' will have 'apple' or 'apply' or any number of longer
        keys that will complete it.  OTOH, the word 'applx' will not have any
        completion keys.  In this situation, we will chop the last letter and
        keep checking for completion keys.  The tail transpose operation is to
        generate transposition candidates.
        '''
        while(len(msword)>=1):
            ss1 = set(list(self._ft.keys(prefix=msword)))
            ss2 = ss1.union(set(list(self._ft.keys(prefix=North.tailswap(msword)))))
            if ss2:
                return ss2
            else:
                msword = North.chop(msword)
                
        return set([])
    
    def _reverse_check(self,msword:str) -> set:
        '''
        Input: mis-spelled word 
        Returns: spelling suggestions
        Assumes beginning of the word is mangled.
        '''
        rmsword = msword[::-1]
        while(len(rmsword)>=1):
            ss1 = set(list(self._rt.keys(prefix=rmsword)))
            ss2 = ss1.union(set(list(self._rt.keys(prefix=North.tailswap(rmsword)))))

            if ss2:
                return set([w[::-1] for w in ss2])
            else:
                rmsword = North.chop(rmsword)
                
        return set([])
    
    @functools.lru_cache(maxsize=10)
    def __call__(self,msword:str,topn:int=2) -> list:
        '''
        Return the combined output of the forward and reverse check.
        '''
        combined_set = self._forward_check(msword).union(self._reverse_check(msword))
        
        # The delete,insert,replace,transpose weights are equal
        # Don't change them unless you know what you are doing.
        dl = lambda w1,w2: damerauLevenshtein(w1, w2, deleteWeight=1, 
                                              insertWeight=1,
                                              replaceWeight=1,
                                              swapWeight=1, similarity=False)
        
        # Sorted combined list of tuples keyed on similarity metric
        combined_tups = sorted([(dl(msword,e),e) for e in combined_set],reverse=False)
        # Separate the words out, take the top n
        combined_list = list(zip(*combined_tups))[1][:min(topn,len(combined_tups))]
        
        if msword in combined_set:  # word is already correct
            return [msword]
        else:
            return combined_list


if __name__ == "__main__":
    
    wordlist = ["sugriva","sugreeva","sugar","superman","super","apple","human","hanuman","horse"]
    misspelledwordlist = ["sgureeva","sugariva","sgurva","hanugreeva","aplpe","hosre","ohrse"]

    my_spelling_suggester = North(wordlist)
    print("Cache test")
    for msw in ["sgureeva"]*5:
        print(msw, timeit.timeit(lambda:my_spelling_suggester(msw)))
    
    class TestFunctions(unittest.TestCase):
        def setUp(self):
            pass
        
        # Check if correct word is in suggestions for the misspelled word.
        def test_forward_check(self):
            self.assertIn("horse",my_spelling_suggester._forward_check("hrose"))
            
        def test_reverse_check(self):
            self.assertIn("horse",my_spelling_suggester._reverse_check("ohrse"))
            
    unittest.main()