# -*- coding: utf-8 -*-

from core.sql.SqlDataMgr import SqlDataMgr
from system.serializable import Serializable
from data.sql_data.PlayerData import PlayerData

def _svr_start():

	SqlDataMgr().connect()
	#SqlDataMgr().register('aaaa', '123123123')
	player = SqlDataMgr().check_sign('aaaa', '123123123')
	player._score = "100"
	player._name = '阿孙'
	SqlDataMgr().save_player_info('aaaa' ,player)
	#ret = Serializable.encode_obj2json(PlayerData())
	#print 'encode_json is ', ret
	#Serializable.decode_json2obj(ret)

def _svr_end():
	SqlDataMgr().shutdown()


if __name__ == '__main__':
	_svr_start()
	_svr_end()