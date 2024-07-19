from __future__ import absolute_import, division, print_function
import sys
import termios
import struct
import fcntl

class ProgressPrinter():
   def __init__(self):
      self._prev = ""
      _, self._cols, _, _ = ioctl_GWINSZ()
      if self._cols == 0:
         # default safe size
         self._cols = 80
         self.istty = False
      else:
         self.istty = True

   def pp(self, msg):
      if not self.istty:
         # normal stdout. print progress status line by line
         print(msg)
      else:
         if len(msg) > self._cols:
            msg = msg[:self._cols - 2]
         if len(self._prev):
            print(end="\r")
            print(" " * len(self._prev), end="\r")
         print(msg, end="")
         self._prev = msg

      sys.stdout.flush()

   def endpp(self):
      if self.istty:
         print()
         self._prev = ""

def ioctl_GWINSZ():
   for f in ( sys.stdin, sys.stdout, sys.stderr ):
      try:
         fd = f.fileno()
         return struct.unpack( 'HHHH', fcntl.ioctl( fd, termios.TIOCGWINSZ,
                               '12345678' ) )
      except:
         pass
   return ( 0, 0, 0, 0 )
