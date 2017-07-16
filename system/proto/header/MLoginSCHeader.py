# -*- coding: utf-8 -*-

from system.proto.Header import Header

class MLoginSCHeader(Header):
	def __init__(self, hid):
		super(MLoginSCHeader, self).__init__(hid)
		self._add_val('name', '131123123124124', 's')
		self._add_val('id', 1, 'i')
		self._add_val('height', '182', 's')
		self._add_val('sex', 'male', 's')
		self._add_val('age', 18, 'i')




if __name__ == '__main__':
	login = MLoginSCHeader(0)
	login.height = '189'
	ret = login.header_encode()
	print 'encode_ret ', ret

	ret = login.header_decode(ret)
	print  login.height