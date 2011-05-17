# -*- coding: UTF-8 -*-
"""
Othman - Quran browser
varuints is a serialization of integer list

Copyright © 2009-2011, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

varuints is a serialization of integer list
based on idea from http://code.google.com/apis/protocolbuffers/docs/encoding.html

but unlike protocolbuffers it preserve order by saving most significant first

in this implementation a single
varuint can be something like

1bbb-bbbb 1bbb-bbbb 0bbb-bbbb

MSB in each byte is "has_more", and rest bits are base-128 int
the above is bbb-bbbb bbb-bbbb bbb-bbbb

use it like this

s=varuints.decode([150,5,7])
a=from_varints(s)

"""

def decode(s):
  v=0
  for c in s:
    c=ord(c)
    v<<=7
    v+=c&127
    if (c&128)==0: yield v; v=0
  if v: raise

def encode(a):
  r=[]
  k=0
  for i in a:
    j,m=0,0
    while(i>0):
      r.insert(k,chr(m|(i&127)))
      i>>=7
      m=128
      j+=1
    if j==0: r.insert(k,'\0'); k+=1
    else: k+=j
  return "".join(r)

def incremetal_encode_list(a, unique=1):
  last=0
  if unique!=1 and unique!=0: raise ValueError
  for i in a:
    if i<last+unique: raise ValueError
    yield i-last-unique
    last=i

def incremetal_decode_list(a, unique=1):
  last=0
  if unique!=1 and unique!=0: raise ValueError
  for i in a:
    j=i+last+unique
    yield j
    last=j
 
def incremetal_encode(a, unique=1):
  return encode(incremetal_encode_list(a, unique))

def incremetal_decode(s, unique=1):
  return incremetal_decode_list(decode(s), unique)


def decode_safe(s):
  v=0
  for c in s:
    c=safe_ord(c)
    v<<=6
    v+=c&63
    if (c&64)==0: yield v; v=0
  if v: raise

def encode_safe(a):
  r=[]
  k=0
  for i in a:
    j,m=0,0
    while(i>0):
      r.insert(k,safe_chr(m|(i&63)))
      i>>=6
      m=64
      j+=1
    if j==0: r.insert(k,safe_chr(0)); k+=1
    else: k+=j
  return "".join(r)


