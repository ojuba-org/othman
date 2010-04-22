# -*- coding: UTF-8 -*-
"""
Othman - Quran browser
Core - python module for accessing Othman API

Copyright © 2009-2010, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

"""
import sys, os, os.path, time
import sqlite3
import struct,zlib
from itertools import izip

def guessDataDir():
  if not hasattr(sys, "frozen"):
    # we are not in py2exe
    f=os.path.abspath(os.path.dirname(__file__))
    d=os.path.join(f, '..', 'othman-data')
    if os.path.exists(d): return d
    d=(f,'..', '..', '..', '..', 'share', 'othman')
    if os.path.exists(d): return d
  # we are in py2exe or DATA can't be located relative to __FILE__
  f=os.path.abspath(os.path.dirname(sys.argv[0]))
  d=os.path.join(f, 'othman-data')
  if os.path.exists(d): return d
  d=os.path.join(f, '..', 'share', 'othman')
  return d

class othmanCore:
  SQL_GET_AYAT='SELECT othmani, imlai FROM Quran WHERE id>=? ORDER BY id LIMIT ?'
  SQL_GET_SURA_INFO='SELECT rowid, sura_name, other_names, makki, starting_row, comment FROM SuraInfo ORDER BY rowid'
  def __init__(self):
    d=guessDataDir()
    db_fn=os.path.join(d,'quran.db')
    self.cn=sqlite3.connect(db_fn)
    self.c=self.cn.cursor()
    l=list(self.c.execute(self.SQL_GET_SURA_INFO).fetchall())
    if len(l)!=114: raise IOError
    self.suraIdByName=dict(((i[1],i[0]) for i in l))
    self.suraInfoById=[list(i[1:])+[0] for i in l]
    for i in range(113):
      self.suraInfoById[i][5]=self.suraInfoById[i+1][3]-self.suraInfoById[i][3]
    self.suraInfoById[-1][5]=6
    self.basmala, self.basmala_imlai=list(self.getAyatIter(1))[0]
    self.basmala=self.basmala[:self.basmala.rfind(' ')]

  def showSunnahBasmala(self, sura):
    return sura!=1 and sura!=9

  def ayaIdFromSuraAya(self, suraId, aya=1):
    """
    suraId: sura number from 1 to 114
    aya: aya number from 1 to the end of the sura
    """
    return self.suraInfoById[suraId-1][3]+aya-1

  def getAyatIter(self, ayaId, number=1):
    """
    return a list of (othmani, imlai) tuples
    """
    return self.c.execute(self.SQL_GET_AYAT, (ayaId,number))

  def getSuraIter(self, suraId, number=0, fromAya=1):
    """
    return a list of (othmani, imlai) tuples for the whole sura
    suraId: sura number from 1 to 114
    number of ayat (0 for the whole sura)
    """
    a=self.suraInfoById[suraId-1]
    m=a[5]
    if number<=0 or number>m: number=m
    return self.getAyatIter(a[3]+fromAya-1, number)

normalize_tb={
65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102, 71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108, 77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114, 83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120, 89: 121, 90: 122,
1600: None, 1569: 1575, 1570: 1575, 1571: 1575, 1572: 1575, 1573: 1575, 1574: 1575, 1577: 1607, 1611: None, 1612: None, 1613: None, 1614: None, 1615: None, 1616: None, 1617: None, 1618: None, 1609: 1575}

def normalize(s): return s.translate(normalize_tb)

class searchIndexerItem:
  def __init__(self, ayaId=None, bits=None):
    if bits:
      self.bits=bits
    else:
      self.bits=[0 for i in range(780)]
      if ayaId: self.setAyaId(ayaId)
  
  def setAyaId(self, ayaId):
    """
    ayaId [1-6236]
    """
    i=ayaId-1
    self.bits[(i>>3)]|=(1<<(i&7))
  
  def __and__(self, y):
    return searchIndexerItem(bits=[i and j for (i,j) in izip(self.bits, y.bits)])
  
  def toAyaIdList(self):
    return filter(lambda k: k,
      sum(map( lambda (i,j):
      [ (j & 1) and (i<<3)+1,
        (j & 2) and (i<<3)+2,
        (j & 4) and (i<<3)+3,
        (j & 8) and (i<<3)+4,
        (j & 16) and (i<<3)+5,
        (j & 32) and (i<<3)+6,
        (j & 64) and (i<<3)+7,
        (j & 128) and (i<<3)+8,
        ]
      ,filter(lambda (ii,jj): jj,enumerate(self.bits))),[]))

class searchIndexer(dict):
  def __init__(self, normalize=normalize):
    dict.__init__(self)
    self.normalize=normalize
    self.maxWordLen=0
  
  def save(self, fn):
    s=""
    m=(self.maxWordLen*2)
    if os.path.exists(fn): os.unlink(fn)
    f=open(fn,"wb+")
    f.write("%d\n" % m)
    fmt="%ds780B" % m
    for w in self:
      a=self[w].bits
      s+=struct.pack(fmt,w.encode('utf8'),*a)
    f.write(zlib.compress(s,9))
    f.close()

  def load(self, fn):
    f=open(fn,"rb")
    m=int(f.readline().strip())
    fmt="%ds780B" % m
    size=struct.calcsize(fmt)
    s=zlib.decompress(f.read())
    for i in range(0,len(s),size):
      u=struct.unpack(fmt,s[i:i+size])
      self[u[0].rstrip('\0').decode('utf8')]=searchIndexerItem(bits=u[1:])

  def find(self, words):
    if not words: return None
    w=self.normalize(words[0])
    x=self.get(w,None)
    if not x: return None
    for w in words[1:]:
      y=self.get(self.normalize(w),None)
      if not y: return None
      x&=y
    return x.toAyaIdList()
  
  def addWord(self, word, ayaId):
    w=self.normalize(word)
    self.maxWordLen=max(self.maxWordLen,len(w))
    if self.has_key(w):
      self[w].setAyaId(ayaId)
    else:
      self[w]=searchIndexerItem(ayaId)


