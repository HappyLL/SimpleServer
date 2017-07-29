# -*- coding: utf-8 -*-

event_listener = {}
event_notify_listener = {}


def add_event_listener(recv_obj, event_id, listener):
	if event_id not in event_listener:
		event_listener[event_id] = {}
	if recv_obj not in event_listener[event_id]:
		event_listener[event_id][recv_obj] = []
	if listener in event_listener[event_id][recv_obj]:
		print '[EventDispathcer][add_event_listener] exist'
		return
	event_listener[event_id][recv_obj].append(listener)
	#print 'event_listener is ',event_listener


def add_notify_event_listener(notify, recv_obj, event_id, listener):
	if event_id not in event_notify_listener:
		event_notify_listener[event_id] = {}
	if notify not in event_notify_listener[event_id]:
		event_notify_listener[event_id][notify] = {}
	if recv_obj not in event_notify_listener[event_id][notify]:
		event_notify_listener[event_id][notify][recv_obj] = []
	if listener in event_notify_listener[event_id][notify][recv_obj]:
		print '[EventDispathcer][add_notify_event_listener] exist'
		return
	#print '[EventDispathcer] add_notify_event_listener is ', event_notify_listener
	event_notify_listener[event_id][notify][recv_obj].append(listener)

def remove_event_listener(recv_obj):
	eids = []
	for eid, recvs in event_listener.iteritems():
		if recv_obj in recvs:
			eids.append(eid)
	for eid in eids:
		del event_listener[eid][recv_obj]
		if len(event_listener[eid]) == 0:
			del event_listener[eid]

	infos = []
	for eid, notifies in event_notify_listener.iteritems():
		for notify, recvs in notifies.iteritems():
			if recv_obj in recvs:
				infos.append((eid, notify, recvs))
	for info in infos:
		eid = info[0]
		notify = info[1]
		recvs = info[2]
		del recvs[recv_obj]
		if len(recvs) == 0:
			del event_notify_listener[eid][notify]
			if len(event_notify_listener[eid]) == 0:
				del event_notify_listener[eid]


def dispatch_event(event_id, notify=None, *args, **kwargs):
	if notify is None:
		if event_id not in event_listener:
			return
		for _, listeners in event_listener[event_id].iteritems():
			for listen in listeners:
				listen(*args, **kwargs)
		return
	if event_id not in event_notify_listener:
		return
	if notify not in event_notify_listener[event_id]:
		return
	for _, listeners in event_notify_listener[event_id][notify].iteritems():
		for listen in listeners:
			listen(*args, **kwargs)


if __name__ == '__main__':
	#add_notify_event_listener(111, 222, 333, lambda : 1 + 1)
	#add_notify_event_listener(111, 666, 333, lambda: 1 + 1)
	#print event_notify_listener
	#remove_event_listener(222)
	#print event_notify_listener
	add_event_listener(111, 222, lambda : 1 + 1)
	add_event_listener(333, 3333, lambda: 1 + 1)
	remove_event_listener(111)
	print event_listener
	print event_notify_listener
