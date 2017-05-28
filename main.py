# -*- coding: utf-8 -*-

from core.sql.SqlDataMgr import SqlDataMgr
from system.serializable import Serializable
from data.sql_data.PlayerData import PlayerData
from core.svr.ServNet import SevrNet
from test.TestSelect import SelectSvr


svr = None

def _svr_start():
	svr = SevrNet()
	svr.init_svr_net()
	svr.start_svr_net()
	#SqlDataMgr().connect()
	#SqlDataMgr().register('aaaa', '123123123')
	#player = SqlDataMgr().check_sign('aaaa', '123123123')
	#player._score = "100"
	#player._name = '阿孙'
	#SqlDataMgr().save_player_info('aaaa' ,player)
	#ret = Serializable.encode_obj2json(PlayerData())
	#print 'encode_json is ', ret
	#Serializable.decode_json2obj(ret)
	# while True:
	# 	cmd = raw_input()
	# 	if cmd == 'exit':
	# 		break
	# svr.end_svr_net()

def _svr_end():
	pass
	#SqlDataMgr().shutdown()


if __name__ == '__main__':
	_svr_start()
	#_svr_end()
	#SelectSvr.start_svr()
	# select_svr = SelectSvr()
	# select_svr.start_svr()