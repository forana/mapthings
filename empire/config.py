properties = {}

def load_properties(filepath):
	file = open(filepath, 'r')
	for line in file:
		if len(line) > 0 and line[0] != "#":
			chunks = line.split("=", 2)
			if len(chunks) == 2:
				key = chunks[0].strip()
				value = chunks[1].strip()
				properties[key] = value
	file.close()

def get_property(key):
	if key in properties:
		return properties[key]
	else:
		raise MissingConfigEntryError(key)

class MissingConfigEntryError(Exception):
	def __init__(self, message):
		self.msg = message
