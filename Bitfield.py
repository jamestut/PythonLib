class Bitfield:
	def __init__(self, v, sz, le=False):
		self.sz = sz
		self.v = v
		self.mask = Bitfield._gen_mask(sz)
		self.le = le
		self._byteorderstr = 'little' if le else 'big'
		assert v <= self.mask

	def __getitem__(self, idx):
		start, sz = self._normalize_index(idx)
		ret = (self.v >> start) & Bitfield._gen_mask(sz)
		return ret

	def __setitem__(self, idx, v):
		start, sz = self._normalize_index(idx)
		contentmask = Bitfield._gen_mask(sz)
		assert v <= contentmask

		contentmask <<= start
		clearmask = self.mask ^ contentmask
		self.v &= clearmask

		self.v |= v << start

	def _normalize_index(self, idx):
		if isinstance(idx, slice):
			start = idx.start
			if start is None:
				start = 0
			stop = idx.stop
			if stop is None:
				stop = self.sz
			sz = stop - start
			assert sz > 0
		else:
			start = idx
			sz = 1
		assert (start + sz) <= self.sz
		return start, sz

	def __int__(self):
		return self.v

	def __bytes__(self):
		return self.v.to_bytes((self.sz + 7) // 8,
			byteorder=self._byteorderstr, signed=False)

	@staticmethod
	def _gen_mask(sz, offset=0):
		assert sz > 0
		ret = (1 << sz) - 1
		return ret << offset
