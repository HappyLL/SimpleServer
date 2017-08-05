# -*- coding: utf-8 -*-

import struct

class Config(object):
	# 协议长
	NET_HEADER_LEN = 4
	NET_HEAD_LENGTH_FORMAT = '=I'
	NET_HID_LENGTH = '=H'

def encode_buffer(buffer, buffer_len):
	header_buffer = struct.pack(Config.NET_HEAD_LENGTH_FORMAT, buffer_len)
	return header_buffer + buffer

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
	if proto_len > (buffer_len - Config.NET_HEADER_LEN) or proto_len == 0:
		#print 'chai bao st proto len is %s buffer_len is %s'%(proto_len, buffer_len)
		return None, buffer
	print 'buffer:len is ', buffer_len
	print 'proto:len is ', proto_len
	st = Config.NET_HEADER_LEN
	ed = proto_len
	wsz = struct.calcsize(Config.NET_HID_LENGTH)
	hbuffer = buffer[st:wsz + st]
	hid = struct.unpack(Config.NET_HID_LENGTH, hbuffer)[0]
	ret = buffer[st:ed + st]
	buffer = buffer[ed + Config.NET_HEADER_LEN:]
	print 'proto ret is ', ret
	print 'header len is ', len(ret)
	return (hid, ret), buffer

def encode_header(header):
	if header is None:
		return
	encode_bin = header.header_encode()
	return encode_buffer(encode_bin, len(encode_bin))
