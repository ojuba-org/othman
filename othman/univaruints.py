# -*- coding: UTF-8 -*-
"""
univaruints is a serialization of integer list
Copyright © 2009-2013, Muayyad Alsadi <alsadi@ojuba.org>



this implementation is unit-tested (by running this module)
"""
import struct, bisect
int64=struct.Struct('>Q')
shifts=[0, 128, 16512, 2113664, 270549120, 34630287488, 4432676798592, 567382630219904, 72624976668147840]
shifts2=shifts[2:]
n_by_chr='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x04\x04\x04\x04\x04\x04\x04\x04\x05\x05\x05\x05\x06\x06\x07\x08'

def bisect_right7(a, x):
    if x<a[3]:
        if x<a[1]:
            if (x<a[0]):
                return 0
            else:
                return 1
        else:
            if x<a[2]:
                return 2
            else:
                return 3
    else:
        if x<a[5]:
            if x<a[4]:
                return 4
            else:
                return 5
        else:
            if x<a[6]:
                return 6
            else:
                return 7



def write(f, s, max_items=0, incremental=0, unique=0, last_item=0):
  """
  encode the sequence s and write the string into the file-like object f

  only max_items are encoded (0 mean infinity)
  if incremental is set to True then the sequence is assumed to be incremental
  which would result in more compact output
  if you know that the sequence is strictly increasing then set unique=1
  """
  # NOTE: below some lookups before loop for optimizations
  fwrite=f.write
  rbisect=bisect_right7 #bisect.bisect_right
  int64pack=int64.pack
  char=chr

  count=0
  last_item-=unique
  for item in s:
    if max_items and count>=max_items: break
    count+=1
    v=item
    if incremental:
      if item<last_item+unique: raise ValueError
      v-=last_item+unique
    if v<128:
      fwrite(char(v))
    else:
      n=rbisect(shifts2, v)+1
      offset=shifts[n]
      v-=offset
      fwrite(char(((0b1111111100000000>>n) & 255) | ( (127>>n) & (v>>(n<<3)) ))+int64pack(v)[8-n:])
    last_item=item
  return count

def read(f, max_items=0, incremental=0, unique=0, last_item=0):
  """
  read and decode sequence at most max_items from the file-like object

  parameters are just like write
  """
  # NOTE: below some lookups before loop for optimizations
  fread=f.read
  int64unpack=int64.unpack
  chr2int=ord

  count=0
  last_item-=unique

  while True:
    if max_items and count>=max_items: break
    ch=fread(1)
    if not ch: break
    count+=1
    o=chr2int(ch)
    if o<128:
      v=o
    else:
      n_ch=n_by_chr[o]
      n=chr2int(n_ch)
      mask=127>>n
      payload=fread(n)
      if len(payload)<n: raise IOError
      v=shifts[n] + (((o & mask)<< (n<<3)) | ( (int64unpack(('\0'*(8-n))+payload))[0] ))
    if incremental: v+=last_item+unique
    yield v
    last_item=v


def decode_single(s):
  """
  return number of bytes consumed and the decoded value
  """   
  o=ord(s[0])
  if o<128: return 1, o
  n_ch=n_by_chr[o]
  n=ord(n_ch)
  mask=127>>n
  return n+1, shifts[n] + (((o & mask)<< (n<<3)) | ( (int64.unpack(('\0'*(8-n))+s[1:n+1]))[0] ))

def decode(s):
  "return a generator that yields all decoded integers"
  offset=0
  while offset<len(s):
    o=ord(chr(s[offset]))
    offset+=1
    if o<128: yield o # just an optimization
    else:
      n_ch=n_by_chr[o]
      n=ord(n_ch)
      mask=127>>n
      yield shifts[n] + (((o & mask)<< (n<<3)) | ( (int64.unpack(('\0'*(8-n)).encode("ISO-8859-1")+s[offset:offset+n]))[0] ))
      offset+=n

def encode_single(v):
    if v<128: return chr(v)
    n=bisect_right7(shifts2, v)+1 #bisect.bisect_right(shifts2, v)+1
    offset=shifts[n]
    v-=offset
    r = chr(((0b1111111100000000>>n) & 255) | ( (127>>n) & (v>>(n<<3)) )).encode("ISO-8859-1") + int64.pack(v)[8-n:]
    return r.decode("ISO-8859-1")

def encode_single_alt(v):
    if v<128: return chr(v) # just an optimization
    offset=128
    m=0
    # enumerate was slower
    #for i,m in enumerate(shifts2):
    for i in shifts2: # although we can use bisect, but we only got 8 elements
        n=m+1
        if v<i:
            v-=offset
            msb=((0b1111111100000000>>n) & 255) | ( (127>>n) & (v>>(n<<3)) )
            p=int64.pack(v)
            return chr(msb) + p[8-n:]
        offset=i
        m+=1
    #m+=1 # if enumerate is used uncomment this line
    v-=offset
    n=m+1
    msb=((0b1111111100000000>>n) & 255) | ( (127>>n) & (v>>(n<<3)) )
    p=int64.pack(v)
    return chr(msb) + p[8-n:]

def encode(a):
    return "".join(map(encode_single, a))

def incremental_encode_list(a, unique=1, last=0):
  if unique!=1 and unique!=0: raise ValueError
  last-=unique
  for i in a:
    if i<last+unique: raise ValueError
    yield i-last-unique
    last=i

def incremental_decode_list(a, unique=1, last=0):
  if unique!=1 and unique!=0: raise ValueError
  last-=unique
  for i in a:
    j=i+last+unique
    yield j
    last=j

def incremental_encode(a, unique=1, last=0):
  return encode(incremental_encode_list(a, unique, last))

def incremental_decode(s, unique=1, last=0):
  return incremental_decode_list(decode(s), unique, last)

#import unittest
#class TestSequenceFunctions(unittest.TestCase):
#    def setUp(self):
#        self.seq = range(10)
#    def test_t1(self):
#        self.assertEqual(x, y)
#        self.assertRaises(TypeError, random.shuffle, (1,2,3))
#        self.assertTrue(element in self.seq)
# in main run unittest.main()

if __name__ == "__main__":
  import time, itertools, random
  from cStringIO import StringIO
  boundary=[(i-1,i,i+1) for i in shifts[1:]]
  boundary=list(itertools.chain(*boundary))
  boundary.insert(0,0)
  print ("simple unit tests...")
  l1=[0,1,100,200,300,500,1000,10000]
  for i in l1:
    print ('before dec:', i, ', hex:', hex(i), ', bin:', bin(i))
    e=encode_single(i)
    print ('after len:',len(e), ', str:', repr(e))
    assert i == decode_single(encode_single(i))[1]
  f=StringIO()
  write(f, l1)
  f.seek(0)
  assert l1==list(read(f))
  print ("boundary unit tests...")
  for i in boundary:
    print ('before dec:', i, ', hex:', hex(i), ', bin:', bin(i))
    e=encode_single(i)
    print ('after len:',len(e), ', str:', repr(e))
    assert i == decode_single(encode_single(i))[1]
  assert boundary == list(decode(encode(boundary)))
  assert boundary == list(incremental_decode(incremental_encode(boundary, unique=0), unique=0))
  assert boundary == list(incremental_decode(incremental_encode(boundary, unique=1), unique=1))
  
  f=StringIO()
  write(f, boundary, 0, 0, 0)
  f.seek(0)
  assert boundary == list(read(f, 0, 0, 0))
  f=StringIO()
  write(f, boundary, 0, 1, 0)
  f.seek(0)
  assert boundary == list(read(f, 0, 1, 0))
  f=StringIO()
  write(f, boundary, 0, 1, 1)
  f.seek(0)
  assert boundary == list(read(f, 0, 1, 1))


  print ("random unit tests...")
  l=[random.randint(0, 5000000) for i in range(1000)]
  s=encode(l)
  l2=list(decode(s))
  assert l2==l
  ll=0
  l=[0]
  for i in range(1000):
    ll+=random.randint(0, 5000000)
    l.append(ll)
  l2=list(incremental_decode(incremental_encode(l, unique=0), unique=0))
  assert l2==l

  ll=0
  l=[0]
  for i in range(1000):
    ll+=random.randint(1, 5000000)
    l.append(ll)
  l2=list(incremental_decode(incremental_encode(l, unique=1), unique=1))
  assert l2==l

  print ("pass")
  print ("performance tests")
  q=struct.Struct('>Q')
  pack=lambda l: ''.join(itertools.imap(lambda i: q.pack(i), l))
  def unpack(s):
      for i in range(0,len(s),8):
          yield q.unpack(s[i:i+8])[0]
  t1=time.time()
  for i in range(1000): list(unpack(pack(boundary)))
  t2=time.time()
  delta_pack=t2-t1
  print ('struct-based done in ', delta_pack)

  f=StringIO()
  t1=time.time()
  for i in range(1000):
    f.seek(0)
    write(f, boundary)
    f.seek(0)
    list(read(f))
  t2=time.time()
  print ('file-like done in ', t2-t1)


  t1=time.time()
  for i in range(1000): list(decode(encode(boundary)))
  t2=time.time()
  delta_our=t2-t1
  print ('we are done in ', delta_our)
  t1=time.time()
  for i in range(1000): encode(boundary)
  t2=time.time()
  delta_our=t2-t1
  print ('we are done in encoding in ', delta_our)
  e=encode(boundary)
  t1=time.time()
  for i in range(1000): list(decode(e))
  t2=time.time()
  delta_our=t2-t1
  print ('we are done in decoding in ', delta_our)

