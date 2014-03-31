"""
Secventa de pasi q-learning:
	Agentul e in starea s
	a <- policy(s)
	s' <- executa a din s
	primeste recompensa r pe baza S -> S' cu a
	actualizeaza Q(s,a) = (1-alpha) Q(s,a) +
	                         alpha( R(s,a,s') + gamma * max( Q(s',a') ) )
	policy(s) poate fi de e.g.:
	eps_greedy pi(s) = { argmax(a) Q(s,a), in eps cazuri
	                     a ales aleator, in 1-eps cazuri
	ideal: * eps e mic initial si creste in timp
	       * alpha e mare initial, scade pe parcurs
"""

from collections import defaultdict
import random

alpha = 0.5
gamma = 0.9
eps = 0.1

# Actions: [stanga, dreapta, trage]
actions = [-1, +1, 0]

# States: stanga, mijloc, dreapta
states = [0, 1, 2]

# States of defender, attacker
def_state = 1
att_state = 1

Q = defaultdict(int)

def get_allowed_actions(state):
	"""All allowed actions from a state. """
	if state == 0:
		return [+1, 0]
	elif state == 1:
		return actions
	elif state == 2:
		return [-1, 0]
	else:
		raise "Not supported state"

def get_attacker_move(def_st, at_st):
	"""Attacker has a rule of moving based on the defender."""

	# Shoot if both on same column.
	if def_st == at_st:
		return actions[2]
	dist = abs(at_st - def_st)

	# Try going left
	dist1 = abs(at_st + actions[0] - def_st)
	if dist1 < dist:
		return actions[0]

	# Then go right
	else:
		return actions[1]

# Get the action that returns a maximum quality
def get_max_action(def_state, att_state):
	"""Get the action that maximizes the Q (quantity).
	   It's a dictionary with the key:
                  (defender_state, attacker_state, action).
	"""
	maximum = -1000
	action = None
	for a in get_allowed_actions(def_state):
		q = Q[(def_state, att_state, a)]
		if maximum < q:
			maximum = q
			action = a
	if action == None:
		raise "Sth is not right"
	return action

def policy(def_state, att_state):
	"""Returns an action based on a policy. Here policy is Eps-greedy."""
	global eps
	eps += 0.04
	if (random.random() <= eps):
		return get_max_action(def_state, att_state)
	# Else pick a random action from all possible actions
	return random.choice(get_allowed_actions(def_state))

def get_reward(def_state, def_action, att_state, att_action):
	new_def_state = def_state + def_action
	new_att_state = att_state + att_action
	if att_action == 0:
		# We loose, attacker shot at us.
		if att_state == new_def_state:
			return -100
		else:
			return 0
	# Defender shoots and wins.
	elif def_action == 0:
		if new_att_state == def_state:
			return +100
		else:
			return 0
	# All move, no loosing
	else:
		return 0

if __name__ == '__main__':
	steps = 10000

	while steps > 0:
		print "states: " + str((def_state, att_state))
		# Attacker move is deterministic in a way, unknown by defender.
		att_action = get_attacker_move(def_state, att_state)
		# Get defender action based on policy.
		def_action = policy(def_state, att_state)
		# Execute action based on state.
		new_def_state = def_state + def_action
		new_att_state = att_state + att_action
		# Check the reward given based on the def_move that was executed.
		reward = get_reward(def_state, def_action, att_state, att_action)
		key = (def_state, att_state, def_action)
		Q[key] = (1-alpha)*Q[key] + alpha * (reward + gamma *
		                                     get_max_action(new_def_state,
		                                                    new_att_state))
		# Update states of both players.
		def_state = new_def_state
		att_state = new_att_state
		steps -= 1
	print Q
