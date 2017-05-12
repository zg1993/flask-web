

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

# class Coffee:
# 	name = ''
# 	price = 0
# 	def __init__(self, name):
# 		self.name = name
# 		self.price = len(name)

# 	def show(self):
# 		print('Coffee Name:{} Price:{}'.format(self.name, self.price))


# name = [0] * 21
# print(name)
# s = '555'

# name[len(s)] += 1
# print(name)
# s1 = '556'
# name[len(s)] += 1
# print(name)

# import re
# prog = re.compile(r'de')
# s = '#define PL_'
# result = prog.search(s)
# print(result)

# import base64

# username = 'zg'
# password = '123'
# print(type(username))
# u = (username+':'+password).encode('utf8')
# print(type(u))
# print(u)
# u1 = u.decode('utf8')
# print(type(u1))
# print(u1)
# u = base64.b64encode(u)
# print(type(u))
# print(u)
# u1 = u.decode('utf8')
# print(type(u1))
# print(u1)




#读取文件提取数字

#f = open('1.txt', 'r')

with open('1.txt', 'r') as f:
	s = f.read()
	print(type(s), len(s))
	l = s.split()
	print(type(l), len(l))






















