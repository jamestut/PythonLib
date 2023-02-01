from collections import abc

def findpath(o, name):
	"""
	This function finds the specified name (str) in the given o (must be a dict or array)
	recursively. The name will be exact match with either a string key or string value.
	"""
	traversed = []
	def findpath_stub(o, name, found):
		if isinstance(o, abc.Sequence):
			# collections indexable by integer
			# warning: this also matches a str!
			enumerator = iter(enumerate(o))
		elif isinstance(o, abc.Mapping):
			# collections representing a dict
			enumerator = iter(o.items())
		else:
			# unknown type
			return

		for k, v in enumerator:
			if k == name:
				# key matched the search term instead of value: continue searching
				found.append(list(traversed))
			traversed.append(k)
			if isinstance(v, str):
				if v == name:
					found.append(list(traversed))
			else:
				findpath_stub(v, name, found)
			traversed.pop()

	ret = []
	findpath_stub(o, name, ret)
	return [''.join(f'[{repr(j)}]' for j in i) for i in ret]
