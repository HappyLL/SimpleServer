# -*- coding: utf-8 -*-

class ComponentA(object):
	ss = 1
	def _init_component(self, *args, **kwargs):
		print '__init__component A'
		self._fff = 1
		self._tory = 2

	def printA(self):
		print 'A'

	def  _destroy_component(self, *args, **kwargs):
		print '__destroy__component B'

class ComponentB(object):
	def _init_component(self, *args, **kwargs):
		print '__init__component B'

	def printB(self):
		print 'B'

	def  _destroy_component(self, *args, **kwargs):
		print '__destroy__component B'