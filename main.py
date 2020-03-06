from construct import *
from os import urandom
from pprint import pprint
from pdb import set_trace
from random import *
from functools import reduce

tests = [
  Struct(
    "a" / Int32ub,
    "b" / Int16ub,
  ),
  Struct(
    "a" / Int32ub,
  ),
  Enum(Int32ub, one = 1, two = 2),
  Enum(Int16ub, one = 1, two = 2, five = 5, ten = 10),
  Struct(
    "a" / Struct(
      "b" / Int32ub
    )
  ),
  Struct(
    "a" / Int16ub,
    "c" / BitStruct(
      "b" / BitsInteger(8)
    )
  )
]

extend = True

def mk_rand(a):
  global extend
  print("--------------")
  print("type: {}".format(type(a)))
  # print("vars: {}")
  # pprint(vars(a))
  # print("dir of renamed: {}")
  # pprint(dir(a))
  if type(a) == Struct:
    print("Struct")
    acc = {}
    temp = [mk_rand(b) for b in a.subcons]
    for d in temp:
      for k,v in d.items():
        acc[k] = v
    ret = acc
  elif type(a) == Renamed:
    print("Renamed")
    ret = {a.name: mk_rand(a.subcon)}
  elif type(a) == Enum:
    print("Enum")
    ret =  choice(list(a.ksymapping.keys()))
  elif type(a) == FormatField:
    print("FormatField")
    ret = a.packer.unpack(urandom(a.length))[0]
  elif type(a) == Transformed:
    print("Transformed")
    ret = mk_rand(a.subcon)
  elif type(a) == BitsInteger:
    print("BitsInteger")
    ret = randrange(2**a.length)
  else:
    print("Unrecognized type {}".format(type(a)))
    if extend:
      pprint(vars(a)) 
    set_trace()
  print("returning {}".format(type(ret)))
  print("+++++++++++++++++++")
  return ret

for i, a in enumerate(tests):
  print("======-- index: {}\n\n".format(i))
  rand_vals = mk_rand(a)
  print("rand_vals is:")
  pprint(rand_vals)

  b = a.build(rand_vals)
  c = a.parse(b)

  print(str(b))
  print(str(c))