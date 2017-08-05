# -*- coding: utf-8 -*-

from logic.ServerManager import ServerManger
from system.proto.header.MPosSCHeader import MPosSCHeader
from system.proto import HeaderConst
from system.proto import Proto
# nosync model
class NoSync(object):
	def __init__(self):
		pass

	def tick(self):
		update_info = ServerManger().pop_data()
		if update_info is None:
			return
		conn = update_info.get('conn')
		pos_header = MPosSCHeader(HeaderConst.HEADER_POS_MSG_ID)
		pos_header.player_id = update_info.get('player_id')
		pos_header.pos_x = update_info.get('pos_x')
		pos_header.pos_y = update_info.get('pos_y')
		encode_bytes = Proto.encode_header(pos_header)
		ServerManger().send_proto_target_to_all(conn, encode_bytes)
