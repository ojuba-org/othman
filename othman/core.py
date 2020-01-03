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
import array
#from itertools import imap
import threading
from functools import reduce
from .univaruints import *
try:
    from itertools import imap
except:
    imap = lambda *args, **kwargs: list(map(*args, **kwargs))



data_dir = None

def cmp(a, b):
    return (a > b) - (a < b)

def guessDataDir():
    global data_dir
    if data_dir: return data_dir
    if not hasattr(sys, "frozen"):
        # we are not in py2exe
        f = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
        d = os.path.join(f, '..', 'othman-data')
        if os.path.exists(d):
            data_dir=os.path.abspath(os.path.realpath(d))
            return data_dir
        d = os.path.join(f,'..', '..', '..', '..', 'share', 'othman')
        if os.path.exists(d):
            data_dir = os.path.abspath(os.path.realpath(d))
            return data_dir
    # we are in py2exe or DATA can't be located relative to __FILE__
    f = os.path.abspath(os.path.realpath(os.path.dirname(sys.argv[0])))
    d = os.path.join(f, 'othman-data')
    if os.path.exists(d):
        data_dir=os.path.abspath(os.path.realpath(d))
        return data_dir
    d = os.path.join(f, '..', 'share', 'othman')
    data_dir = os.path.abspath(os.path.realpath(d))
    return data_dir

def cmp_bisect_right(ccmp, a, x, lo=0, hi=None):
    """
        same as bisect.bisect but uses custom cmp function
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) >> 1
        if ccmp(a[mid], x) > 0:
            hi = mid # ie. if x < a[mid]
        else:
            lo = mid + 1
    return lo

def cmp_bisect_left(ccmp, a, x, lo=0, hi=None):
    """
        same as bisect.bisect_left but uses custom cmp function
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) >> 1
        if ccmp(x, a[mid]) > 0:
            lo = mid + 1 # ie. if a[mid] < x
        else:
            hi = mid
    return lo


class othmanCore(object):
    SQL_GET_AYAT = 'SELECT othmani, imlai FROM Quran WHERE id>=? ORDER BY id LIMIT ?'
    SQL_GET_SURA_INFO = 'SELECT rowid, sura_name, other_names, makki, starting_row, comment FROM SuraInfo ORDER BY rowid'
    def __init__(self, load_ix=True):
        self.data_dir = d = guessDataDir()
        self.db_fn = db_fn = os.path.join(d, 'quran.db')
        self._cn = {}
        cn = self._getConnection()
        l = list(cn.execute(self.SQL_GET_SURA_INFO).fetchall())
        if len(l) != 114:
            raise IOError
        self.suraIdByName = dict(((i[1], i[0]) for i in l))
        self.suraInfoById = [list(i[1:]) + [0] for i in l]
        for i in range(113):
            self.suraInfoById[i][5] = self.suraInfoById[i + 1][3] - self.suraInfoById[i][3]
        self.suraInfoById[-1][5] = 6
        self.basmala, self.basmala_imlai = list(self.getAyatIter(1))[0]
        self.basmala = self.basmala[:self.basmala.rfind(' ')]
        self.ix = None
        if load_ix:
            self.ix = searchIndexer()

    def _getConnection(self):
        n = threading.current_thread().name
        if n in self._cn.keys():
            r = self._cn[n]
        else:
            r = sqlite3.connect(self.db_fn)
            self._cn[n] = r
        return r

    def showSunnahBasmala(self, sura):
        return sura != 1 and sura != 9

    def suraAyaFromAyaId(self, ayaId):
        sura = cmp_bisect_right(lambda i, j: cmp(i[3], j), self.suraInfoById, ayaId)
        aya = ayaId - self.suraInfoById[sura-1][3] + 1
        return sura, aya

    def ayaIdFromSuraAya(self, suraId, aya = 1):
        """
            suraId: sura number from 1 to 114
            aya: aya number from 1 to the end of the sura
        """
        return self.suraInfoById[suraId-1][3] + aya - 1

    def getAyatIter(self, ayaId, number = 1):
        """
            return a list of (othmani, imlai) tuples
        """
        return self._getConnection().execute(self.SQL_GET_AYAT, (ayaId,number))

    def getSuraIter(self, suraId, number=0, fromAya=1):
        """
            return a list of (othmani, imlai) tuples for the whole sura
            suraId: sura number from 1 to 114
            number of ayat (0 for the whole sura)
        """
        a = self.suraInfoById[suraId - 1]
        m = a[5]
        if number <= 0 or number > m:
            number = m
        return self.getAyatIter(a[3] + fromAya - 1, number)

normalize_tb={
    65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102,
    71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108,
    77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114,
    83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120,
    89: 121, 90: 122, 1600: None, 1569: 1575, 1570: 1575,
    1571: 1575, 1572: 1575, 1573: 1575, 1574: 1575, 1577: 1607,
    1611: None, 1612: None, 1613: None, 1614: None, 1615: None,
    1616: None, 1617: None, 1618: None, 1609: 1575}

def normalize(s):
    return s.translate(normalize_tb)

class searchIndexerItem(set):
    def __init__(self, *a):
        set.__init__(self, *a)

    def __or__(self, y):
        return self.union(y)

    def __and__(self, y):
        return self.intersection(y)

    def toAyaIdList(self):
        l = list(self)
        l.sort()
        return l

class searchIndexer:
    def __init__(self, unlink = False, normalize = normalize):
        d = guessDataDir()
        self.db_fn = fn = os.path.join(d, "ix.db")
        if unlink and os.path.exists(fn):
            os.unlink(fn)
        self._cn = {}
        self.d = {}
        self.normalize = normalize
        self.maxWordLen = 0
        self.term_vectors_size = 0
        self.terms_count = 0

    def _getConnection(self):
        n = threading.current_thread().name
        if n in self._cn.keys():
            r = self._cn[n]
        else:
            r = sqlite3.connect(self.db_fn)
            self._cn[n] = r
        return r

    def save(self):
        cn = self._getConnection()
        c = cn.cursor()
        c.execute('CREATE TABLE ix (w TEXT PRIMARY KEY NOT NULL, i BLOB)')
        for w in self.d:
            b = incremental_encode(self.d[w].toAyaIdList())
            self.term_vectors_size += len(b)
            c.execute( 'INSERT INTO ix VALUES(?,?)', (w, sqlite3.Binary(b.encode("ISO-8859-1"))) )
        self.terms_count = len(self.d.keys())
        cn.commit()

    def _itemFactory(self, r):
        a = incremental_decode(r[1])
        return r[0], searchIndexerItem(a)

    def _itemFactory2(self, r):
        a = incremental_decode(r[1])
        return searchIndexerItem(a)

    def get(self, w):
        cn = self._getConnection()
        r = cn.execute('SELECT w, i FROM ix WHERE w=?', (w,)).fetchone()
        if not r:
            return None, None
        return self._itemFactory(r)

    def getPartial(self, w, withWords=False):
        if "%" in w or "_" in w:
            return [] # special chars
        cn = self._getConnection()
        W = "%" + w + "%"
        f = withWords and self._itemFactory or self._itemFactory2
        r = cn.execute('SELECT w, i FROM ix WHERE w LIKE ?', (W, ))
        if not r:
            return []
        return imap(lambda i: f(i), r)

    def find(self, words):
        if not words:
            return None
        w = self.normalize(words[0])
        W, x = self.get(w)
        if not x:
            return None
        for w in words[1:]:
            W, y = self.get(self.normalize(w))
            if not y:
                return None
            x &= y
        return x.toAyaIdList()

    def findPartial(self, words):
        if not words:
            return None
        w = self.normalize(words[0])
        x = reduce( lambda a,b: a|b, self.getPartial(w), searchIndexerItem() )
        for W in words[1:]:
            w = self.normalize(W)
            y = reduce( lambda a,b: a|b, self.getPartial(w), searchIndexerItem() )
            x &= y
        try :
            return x.toAyaIdList()
        except AttributeError:
            x2 = searchIndexerItem(x)
            return x2.toAyaIdList()

    def addWord(self, word, ayaId):
        w = self.normalize(word)
        #if not w: print word; return
        self.maxWordLen = max(self.maxWordLen,len(w))
        if w in self.d.keys():
            self.d[w].add(ayaId)
        else:
            self.d[w] = searchIndexerItem((ayaId,))


