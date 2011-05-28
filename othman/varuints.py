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

in this implementation a single varuint can be something like

1xxx-xxxx 1xxx-xxxx 0xxx-xxxx

MSB in each byte is "has_more", and rest bits are base-128 int
the above is xxx-xxx xxx-xxxx xxx-xxxx


0xxx-xxxx is 0-127

1xxx-xxxx 0xxx-xxxx  is 128-16511

and so on

use it like this

s=varuints.decode([150,5,7])
a=from_varints(s)

"""

def decode(s):
  v=0
  for c in s:
    c=ord(c)
    v+=(c&127)
    if (c&128)==0: yield v; v=0
    else: v+=1
    v<<=7
  if v: raise ValueError

def encode(a):
  r=[]
  k=0
  for i in a:
    j,m=0,0
    while(1):
      r.insert(k,chr(m|(i&127)))
      m=128
      j+=1
      i>>=7
      if i==0: break
      i-=1
    k+=j
  return "".join(r)

def write(f, a):
  """encode members of a and write them to file f and return the number of bytes written"""
  s=encode(a)
  f.write(s)
  return len(s)

def read(f, limit=1):
  """read and decode up to limit integers from file f and return them"""
  v,n=0,0
  while(n<limit):
    c=f.read(1)
    if c=='': raise ValueError
    c=ord(c)
    v+=(c&127)
    if (c&128)==0: yield v; v=0; n+=1
    else: v+=1
    v<<=7
  if v: raise ValueError

def read_single(f):
  """read and decode a single varuint from file f and return it"""
  return read(f,1).next()


def incremental_encode_list(a, unique=1, last=0):
  if unique!=1 and unique!=0: raise ValueError
  for i in a:
    if i<last+unique: raise ValueError
    yield i-last-unique
    last=i

def incremental_decode_list(a, unique=1, last=0):
  if unique!=1 and unique!=0: raise ValueError
  for i in a:
    j=i+last+unique
    yield j
    last=j
 
def incremental_encode(a, unique=1, last=0):
  return encode(incremental_encode_list(a, unique, last))

def incremental_decode(s, unique=1, last=0):
  return incremental_decode_list(decode(s), unique, last)

def incremental_write(f, a, unique=1, last=0):
  return write(f, incremental_encode_list(a, unique, last))

def incremental_read(f, unique=1, limit=1, last=0):
  return incremental_decode_list(read(f, limit), unique, last)


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


