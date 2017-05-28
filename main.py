# -*- coding: utf-8 -*-
import time
from core.Server import Server

svr = Server()
frame_tm = 1

if __name__ == '__main__':
	svr.svr_start()
	while True:
		time.sleep(frame_tm)
		svr.tick()

	svr.svr_end()