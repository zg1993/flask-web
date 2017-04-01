

class A():
	a = ''

	@property
	def name(self):
		return self.name


	@name.setter
	def name(self, name):
		self.a = name


a = A(name='aaa')
print(a.name)


