class FileToList:
	"""docstring for FileToList"""
	def __init__(self, file_input):	
		print "get3!"
		print "file_input:", file_input
		filename = str(file_input)
		print "get4!"
		print "filename:", filename
		file = open(filename, "r")
		print "get5!"
		self.content = file.read()
		print "get6!"
		file.close()

	def to_list(self):
		content_list = self.content.split("\n")
		return content_list
