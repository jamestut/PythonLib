from collections import namedtuple

# 'cap_size' is implied in len(data)!
PcapItem = namedtuple('PcapItem', ['ts_sec', 'ts_usec', 'orig_size', 'data'])

class Pcap:
	def __init__(self, f):
		"""
		Args:
		  f: A binary file-like object
		"""
		self._f = f
		# check magic
		magic = f.read(4)
		if magic != b'\xd4\xc3\xb2\xa1':
			raise ValueError("Unsupported PCAP format. Only little-endian format is supported!")
		# other nice-to-know details
		self.major_ver = int.from_bytes(f.read(2), byteorder='little')
		self.minor_ver = int.from_bytes(f.read(2), byteorder='little')
		self.utc_offset = int.from_bytes(f.read(4), byteorder='little', signed=True)
		# some other infos that we don't really need
		f.read(4) # sigfigs
		self.packet_count = int.from_bytes(f.read(4), byteorder='little')
		self.data_link_type = int.from_bytes(f.read(4), byteorder='little')

	def __len__(self):
		return self.packet_count

	def __iter__(self):
		return self

	def __next__(self):
		# read the next record
		def try_read(sz):
			assert sz
			rd = self._f.read(sz)
			if not len(rd):
				# assume file finished
				raise StopIteration
			return rd

		ts_sec = int.from_bytes(try_read(4), byteorder='little')
		ts_usec = int.from_bytes(try_read(4), byteorder='little')
		cap_size = int.from_bytes(try_read(4), byteorder='little')
		orig_size = int.from_bytes(try_read(4), byteorder='little')
		data = try_read(cap_size)
		return PcapItem(ts_sec, ts_usec, orig_size, data)
