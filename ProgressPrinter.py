from __future__ import absolute_import, division, print_function
import TerminalUtil
import sys

class ProgressPrinter():
   def __init__(self):
      self._prev = ""
      self.istty = TerminalUtil.isTerminalRealSafe()
      if self.istty:
         _, self._cols, _, _ = TerminalUtil.ioctl_GWINSZ();

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
