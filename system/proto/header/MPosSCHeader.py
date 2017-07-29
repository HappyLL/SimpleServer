# -*- coding: utf-8 -*-

from system.proto.Header import Header


class MPosSCHeader(Header):
	def __init__(self, hid):
		super(MPosSCHeader, self).__init__(hid)
		self._add_val('pos_x', '0', 'f')
		self._add_val('pos_y', '0', 'f')
		self._add_val('v_x', '0', 'f')
		self._add_val('v_y', '0', 'f')