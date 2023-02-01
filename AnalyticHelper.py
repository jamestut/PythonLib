"""
Contains various functions to make it more convenient to analyse dictionary dumps on
Python shell.
"""

from collections import abc
import json

class DynamicNamedTuple:
  def __str__(self):
    return str(self.__dict__)

  def __repr__(self):
    return str(self)

def convert(v):
  """
  Make a new copy of v
  """
  if isinstance(v, (list, tuple)):
    ret = [convert(i) for i in v]
    return ret
  elif isinstance(v, dict):
    ret = DynamicNamedTuple()
    for k, v in v.items():
      setattr(ret, k, convert(v))
    return ret
  else:
    # no copy, no modification, just return the same thing
    return v

def fromjsonfile(f):
  def _cvt(fh):
    return convert(json.load(fh))

  if isinstance(f, abc.Sequence):
    # string == file name
    with open(f, 'r') as fh:
      return _cvt(fh)
  # must be a file handle already otherwise
  return _cvt(fh)

def fromjson(d):
  return convert(json.loads(d))
