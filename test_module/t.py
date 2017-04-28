

# class A():
# 	a = ''

# 	@property
# 	def name(self):
# 		return self.name


# 	@name.setter
# 	def name(self, name):
# 		self.a = name

# from datetime import datetime
# from random import seed, randint

# class C():
# 	names = 'aaa'
# 	def __init__(self, name):
# 		print(self.names)
# 		self.name = name


# c = C('zg')

# d = {'name': 'zg'}
# a = hasattr(d, 'name')
# print(dir(d))
# print(a)

class Coffee:
	name = ''
	price = 0
	def __init__(self, name):
		self.name = name
		self.price = len(name)

	def show(self):
		print('Coffee Name:{} Price:{}'.format(self.name, self.price))


name = [0] * 21
print(name)
s = '555'

name[len(s)] += 1
print(name)
s1 = '556'
name[len(s)] += 1
print(name)




























