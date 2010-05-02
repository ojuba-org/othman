#! /usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os, os.path, time
from othman.core import othmanCore, searchIndexer

q=othmanCore(False)
ix=searchIndexer(True)
for n,(o,i) in enumerate(q.getAyatIter(1, 6236)):
  for w in i.split(): ix.addWord(w,n+1)
d=os.path.dirname(sys.argv[0])
ix.save()

