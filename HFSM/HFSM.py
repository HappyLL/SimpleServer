# -*- coding: utf-8 -*-

# 分层状态机

HFSM_ROOT_STATE_ID = 1
HFSM_A_STATE_ID = 2
HFSM_B_STATE_ID = 3
HFSM_C_STATE_ID = 4
HFSM_D_STATE_ID = 5
HFSM_E_STATE_ID = 6


class IState(object):
	def __init__(self, state_id):
		self._state_id = state_id
		self._active = False
		self._parent = None
		print 'Init State Name is ', self.__class__.__name__

	def enter(self, context):
		if self._active:
			return
		print 'Enter State Name is ',self.__class__.__name__
		self._active = True


	def exit(self):
		if not self._active:
			return
		print 'Exit State Name is ', self.__class__.__name__
		self._active = False

	@property
	def active(self):
		return self._active

	def tick(self):
		pass

	def destroy(self):
		self._active = False
		self._parent = None
		self._state_id = None
		print 'Destroy State Name is ', self.__class__.__name__

	@property
	def state_id(self):
		return self._state_id

	@property
	def parent(self):
		return self._parent

	@parent.setter
	def parent(self, value):
		self._parent = value

class RootState(IState):
	def __init__(self):
		super(RootState, self).__init__(HFSM_ROOT_STATE_ID)
		self._active = True

class AState(IState):
	def __init__(self):
		super(AState, self).__init__(HFSM_A_STATE_ID)

class BState(IState):
	def __init__(self):
		super(BState, self).__init__(HFSM_B_STATE_ID)

class CState(IState):
	def __init__(self):
		super(CState, self).__init__(HFSM_C_STATE_ID)

class DState(IState):
	def __init__(self):
		super(DState, self).__init__(HFSM_D_STATE_ID)

class EState(IState):
	def __init__(self):
		super(EState, self).__init__(HFSM_E_STATE_ID)

class HFSM(object):
	def __init__(self):
		self.mp_state = {}
		self.current_state = None

	def get_current_state(self):
		return self.current_state

	def get_state(self, state_id):
		return state_id in self.mp_state and self.mp_state[state_id]

	def translate_to(self, state_id, context=None):
		# 通过当前的state_id 去找第一个active为True的节点则为与
		# current的公共节点
		target_state = self.mp_state.get(state_id)
		if not target_state:
			print 'error the empty state state id is ',state_id
			return
		tmp_state = target_state
		active_lists = [tmp_state, ]
		while not tmp_state.active:
			if not tmp_state.parent:
				print 'error the state parent is null and active is false ',tmp_state
				return
			tmp_state = tmp_state.parent
			active_lists.insert(0, tmp_state)
		while self.current_state != tmp_state and self.current_state:
			self.current_state.exit()
			self.current_state = self.current_state.parent
		for _, state in enumerate(active_lists):
			state.enter(context)
		self.current_state = target_state

	def add_state(self, state, parent):
		self.mp_state[state.state_id] = state
		state.parent = parent

	def remove_state(self, state_id):
		if state_id not in self.mp_state:
			return
		state = self.mp_state[state_id]
		state.destroy()
		del self.mp_state[state_id]

class GameHFSMController(HFSM):
	HFSM_DATA = {
		'AState': AState,
		'BState': BState,
		'CState': CState,
		'DState': DState,
		'EState': EState,
		'RootState': RootState,
	}
	HFSM_RELATION = {
		'RootState': {
			'AState': {
				'BState': {},
				'CState': {},
			},
			'DState': {
				'EState': {},
			}
		}
	}

	def __init__(self):
		super(GameHFSMController, self).__init__()

	def build_hfsm_tree(self):
		origin_state_cache = [(['RootState'], None, GameHFSMController.HFSM_RELATION), ]
		while len(origin_state_cache) > 0:
			new_state_cache = []
			for _, state_info in enumerate(origin_state_cache):
				state_parent = state_info[1]
				state_relations = state_info[2]
				for _, state_name in enumerate(state_info[0]):
					cls_state = GameHFSMController.HFSM_DATA[state_name]
					state = cls_state()
					self.add_state(state, state_parent)
					relations = state_relations[state_name]
					childs = relations.keys()
					if len(childs) > 0:
						new_state_cache.append([childs, state, relations])
			origin_state_cache = new_state_cache

	def destroy_hfsm_tree(self):
		self.translate_to(HFSM_ROOT_STATE_ID)
		self.mp_state = None
		self.current_state = None

	def print_hfsm_tree(self):
		for k, v in self.mp_state.iteritems():
			print 'state_id ', k
			print 'state_name ', v.__class__.__name__
			print 'state_parent ', v.parent and v.parent.__class__.__name__
			print 'state_active ', v.active

	def tick(self):
		# tick需要从子节点到父节点的tick
		pass

if __name__ == '__main__':
	hfms_tree = GameHFSMController()
	hfms_tree.build_hfsm_tree()
	hfms_tree.translate_to(HFSM_ROOT_STATE_ID)
	#hfms_tree.print_hfsm_tree()
	hfms_tree.translate_to(HFSM_C_STATE_ID)
	print '**************************'
	#hfms_tree.print_hfsm_tree()
	hfms_tree.translate_to(HFSM_D_STATE_ID)
	#print '**************************'
	#hfms_tree.print_hfsm_tree()
	hfms_tree.destroy_hfsm_tree()

