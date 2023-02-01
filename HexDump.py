def hexdump(data, show_offset=True, colsz=0x10):
	"""
	pretty print bytearray
	"""
	if colsz > 0xFF:
		assert ValueError("Maximum width is 255 cols!")

	count = len(data)
	cw_pad = len(f"{count:x}")
	# 2 + 2 chars for "0x" and ": "
	cw = cw_pad + 4

	# print header
	if show_offset:
		print(" " * cw, end="")
		header = " ".join((f"{i:02X}" for i in range(colsz)))
		print(header)
		print("=" * (len(header) + cw))

	# print contents
	printed = 0
	while printed < count:
		if show_offset:
			print("0x{0:0{1}x}: ".format(printed, cw_pad), end="")
		amm = min(colsz, count - printed)
		print(*[f"{data[i]:02x}" for i in range(printed, printed + amm)])
		printed += amm

def hexdump_simple(data, spacing=False, uppercase=False):
	"""
	convert bytearray to a hex string
	"""
	delim = " " if spacing else ""
	fmt = "{:02X}" if uppercase else "{:02x}"
	return delim.join((fmt.format(i) for i in data))

def hexstring_to_ba(s):
	"""
	basically the inverse of hexdump_simple
	"""
	s = ''.join(s.split())
	if len(s) % 2:
		raise ValueError("String size must be even")
	ret = bytearray(len(s) // 2)
	for i in range(len(ret)):
		ret[i] = int(s[i*2:i*2+2], 16)
	return ret
