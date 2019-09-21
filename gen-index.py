#! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function

import sys, os, os.path, time
from othman.core import othmanCore, searchIndexer

q = othmanCore(False)
ix = searchIndexer(True)
wc = 0
for n,(o,i) in enumerate(q.getAyatIter(1, 6236)):
    for w in i.split():
        ix.addWord(w,n+1)
        wc += 1
d = os.path.dirname(sys.argv[0])
ix.save()
print("got %d words, %d terms (max term length=%d character, term vectors size=%d bytes)." % (wc, ix.terms_count, ix.maxWordLen, ix.term_vectors_size))


