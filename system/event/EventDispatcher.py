# -*- coding: utf-8 -*-

event_listener = {}


def add_event_listener(recv_obj, event_id, listener):
	if event_id not in event_listener:
		event_listener[event_id] = {}
	if recv_obj not in event_listener[event_id]:
		event_listener[event_id][recv_obj] = []
	if listener in event_listener[event_id][recv_obj]:
		print '[EventDispathcer][add_event_listener] exist'
		return
	event_listener[event_id][recv_obj].append(listener)


def remove_event_listener(recv_obj):
	eids = []
	for eid, recvs in event_listener.iteritems():
		if recv_obj in recvs:
			eids.append(eid)
	for eid in eids:
		del event_listener[eid][recv_obj]


def dispatch_event(event_id, *args, **kwargs):
	if event_id not in event_listener:
		return

	for _, listeners in event_listener[event_id].iteritems():
		for listen in listeners:
			listen(*args, **kwargs)
