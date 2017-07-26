# -*- coding: utf-8 -*-

net_event_listener = {}


def add_net_event_listener(net_event_id, listener):
	if net_event_id not in net_event_listener:
		net_event_listener[net_event_id] = []
	if listener in net_event_listener[net_event_id]:
		print '[EventDispathcer][add_net_event_listener] exist'
		return
	net_event_listener[net_event_id].append(listener)


def remove_net_event_listener(net_event_id):
	if net_event_id not in net_event_listener:
		return
	del net_event_listener[net_event_id]


def dispatch_event(net_event_id, *args, **kwargs):
	if net_event_id not in net_event_listener:
		return

	for listener in net_event_listener[net_event_id]:
		listener(*args, **kwargs)