# -*- coding: utf-8 -*-
def importall():
	from test import TestSelect
	return locals().values()

class A(object):
	aaa = 1
	def printA(self):
		print 'A'

class B(A):
	def printB(self):
		print 'B'

if __name__ == '__main__':
	values = importall()
	print type(values[0]) == 'module'
	import inspect
	print inspect.getmembers(B, lambda x: type(x) is int)
