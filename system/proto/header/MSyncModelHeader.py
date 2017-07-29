# -*- coding: utf-8 -*-

from system.proto.Header import Header

class MSyncModelHeader(Header):
	def __init__(self, hid):
		super(MSyncModelHeader, self).__init__(hid)
		self._add_val('sync_model', 0, 'i')
