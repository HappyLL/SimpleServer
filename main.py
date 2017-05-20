# -*- coding: utf-8 -*-

from core.sql.SqlDataMgr import SqlDataMgr


def _svr_start():
	SqlDataMgr().connect()
	SqlDataMgr().register('111122', '123123123')

def _svr_end():
	SqlDataMgr().shutdown()


if __name__ == '__main__':
	_svr_start()
	_svr_end()