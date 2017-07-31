# -*- coding: utf-8 -*-

from system.proto.Header import Header


class MLoginSCHeader(Header):
	def __init__(self, hid):
		super(MLoginSCHeader, self).__init__(hid)
		self._add_val('player_id', 1, 'i')
		self._add_val('pos_x', 0, 'f')
		self._add_val('pos_y', 0, 'f')


if __name__ == '__main__':
	login = MLoginSCHeader(0)
	ret = login.header_encode()
	from system.proto import Proto
	bytes_len = len(ret)
	encode_bytes = Proto.encode_buffer(ret, bytes_len)
	decode_bytes, _ = Proto.decode_buffer(encode_bytes, len(encode_bytes))
	ret = login.header_decode(decode_bytes[1])
	print login.player_id