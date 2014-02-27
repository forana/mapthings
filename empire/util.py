""" List optimized for contains checks. Assumes items will not be removed."""
class IndexedList(list):
	def __init__(self):
		list.__init__(self, [])
		self.backing_set = set()

	def append(self, item):
		self.backing_set.add(item)
		list.append(self, item)

	def __contains__(self, item):
		return item in self.backing_set
