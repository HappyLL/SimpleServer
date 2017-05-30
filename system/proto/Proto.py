# -*- coding: utf-8 -*-

import struct

class Config(object):
	# 协议长
	NET_HEADER_LEN = 4
	NET_HEAD_LENGTH_FORMAT = '=I'

def encode_buffer(buffer, buffer_len):
	pass


# 获取一个完整的proto
def decode_buffer(buffer, buffer_len):
	if Config.NET_HEADER_LEN > buffer_len:
		return None, buffer
	proto_len = buffer[:Config.NET_HEADER_LEN]
	# unpack 返回的是一个tuple
	try:
		proto_len = struct.unpack(Config.NET_HEAD_LENGTH_FORMAT, proto_len)[0]
	except Exception, e:
		raise ValueError('proto is error exc is', e)
	# 取完整的
	if proto_len > (buffer_len - Config.NET_HEADER_LEN):
		print 'chai bao st proto len is %s buffer_len is %s'%(proto_len, buffer_len)
		return None, buffer
	st = Config.NET_HEADER_LEN
	ed = Config.NET_HEADER_LEN + proto_len
	ret = buffer[st:ed]
	buffer = buffer[ed:]
	print 'proto ret is ', ret
	return ret, buffer