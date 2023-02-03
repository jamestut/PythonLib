"""
Like io.BytesIO, but allocate or reallocate only when asked to!
"""

from io import RawIOBase
import sys

class BIO(RawIOBase):
	def __init__(self, sz):
		self._data = bytearray(sz)
		self._pos = 0
		self._limit = None

	def flush(self):
		# do nothing
		pass

	def close(self):
		# do nothing
		pass

	def readable(self):
		return True

	def seekable(self):
		return True

	def writable(self):
		return True

	def tell(self):
		return self._pos

	def set_limit(self, lim=None):
		if lim is not None:
			if lim < 0 or lim > len(self._data):
				raise ValueError("Limit must be at most current size")
		self._limit = lim

	def seek(self, pos, whence=0):
		if whence == 0:
			pass
		elif whence == 1:
			pos = self._pos + pos
		elif whence == 2:
			pos = len(self) + pos
		else:
			raise ValueError("Unsupported whence")

		if not pos and not len(self):
			pass
		elif pos > len(self) or pos < 0:
			raise ValueError("Invalid resulting position")

		self._pos = pos

	def read(self, size=-1):
		newpos = len(self)
		if size >= 0:
			newpos = min(newpos, self._pos + size)
		begin = self._pos
		ret = bytes(self._data[self._pos:newpos])
		self._pos = newpos
		return ret

	def readall(self):
		return self.read()

	def readinto(self, b):
		newpos = self._pos + len(b)
		if newpos > len(self):
			raise ValueError("Not enough data to read into")
		b[0:] = self._data[self._pos:newpos]
		self._pos = newpos

	def truncate(self, sz):
		if sz <= len(self._data):
			raise ValueError("New size must be bigger than current buffer")
		# 2, because one in self, one while being handled by getrefcount itself
		if sys.getrefcount(self._data) > 2:
			raise BufferError("Existing export of buffer: cannot be resized")
		self._data += bytearray(sz - len(self._data))

	def write(self, b):
		newpos = self._pos + len(b)
		if newpos > len(self):
			raise BufferError("Written data to big for buffer. Please resize.")
		self._data[self._pos:newpos] = b
		self._pos = newpos

	def capacity(self):
		return len(self._data)

	def getbuffer(self):
		return memoryview(self._data)[:len(self)]

	def __len__(self):
		return len(self._data) if self._limit is None else self._limit
