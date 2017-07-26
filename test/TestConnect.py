# -*- coding: utf-8 -*-

import socket

def func():
	from system.proto import Proto
	from system.proto.header.MLoginSCHeader import MLoginSCHeader
	from system.proto import HeaderConst
	hd = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
	hd_bin = hd.header_encode()
	#hd.header_decode(hd_bin)
	print 'hd_bin is ', hd_bin
	en_bin = Proto.encode_buffer(hd_bin, len(hd_bin))
	print 'en_bin is ', en_bin
	print 'en_bin len is ', len(en_bin)
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.connect(('127.0.0.1', 8888))

	while True:
		cnt = sk.send(en_bin)
		if cnt < len(en_bin):
			en_bin = en_bin[cnt:]
		else:
			break
	print 'send all'


if __name__ == '__main__':
	func()
