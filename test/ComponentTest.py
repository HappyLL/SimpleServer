# -*- coding: utf-8 -*-

from component import classutils
from test import Component_A

@classutils.component_cls(Component_A.ComponentA, Component_A.ComponentB)
class ComponentTest(object):
	def __init__(self):
		self._call_component("init")

	def destroy(self):
		self._call_component("destroy")

if __name__ == '__main__':
	test_component = ComponentTest()
	test_component.printA()
	test_component.printB()
	test_component._fff += 1
	print 'test_component _fff ', test_component._fff
	ComponentTest._del_component(Component_A.ComponentB)
