from graph import Graph, dotdict

from itertools import combinations
from random import sample, randint
import numpy as np

from pynput.keyboard import Key, Listener

class Mind(Graph):

	def __init__(self, kwargs):
		super().__init__(kwargs)
		# for k, v in self.roles.items():
		# 	print('Role:',k)
		# 	for i in v:
		# 		print(i)
		# 	print('-------------------------')
		
		self.index = -1
		self.blocked = False

		# init output and feedback to zero
		for i, o, f in zip(self.roles.input, self.roles.output, self.roles.feedback):
			i.pack, o.pack, f.pack = 0, 0, 0
		
		self.print_all()

		
	def get_input(self):
		self.index += 1
		if self.index == len(self.input_vals): self.index = 0
		return self.input_vals[self.index]
	
	@staticmethod
	def breadth(node):
		pass


	def input_incoming(self):
		self.blocked = True
		# get input, set it to input node pack
		if not len(input_nodes) == len(self.roles.input):
			raise ValueError(f'Length of input pack list is not correct, should be {len(input_nodes)}, was found to be {len(self.roles.input)}')
		
		for input_node, val in zip(self.roles.input, self.get_input()):
			print('INPUT node:',input_node.id)
			input_node.pack += val

		self.think_it_out()


	def think_it_out(self):
		self.blocked = True
		# OVERFLOW RULE ::
		"""
		if pack overflows single digit,
		subtract multiple of 9 till value is < 10
		fire the final pack value
		"""
		
		for node in self.nodes: # self thinking
			print(f'{node.role} node: {node.id}')

			if node.pack > 9:
				while node.pack > 9: node.pack -= 9

				for edge in node.edges:
					_id_two = edge.ends.copy()
					_id_two.remove(node.id)
					_id_two = _id_two[0]

					self.nodes[_id_two].pack += node.pack

		feed_sum = 0
		for output_node in self.roles.output:
			# record outputs
			self.outputs[output_node.id].append(output_node.pack)
			# sum all output node packs
			feed_sum += output_node.pack

		# then add it to all feedback nodes
		for feedback_node in self.roles.feedback:
			feedback_node.pack += feed_sum

		self.blocked = False


	def propagate(self): # BFS
		if not self.blocked:
			key = input('Enter choice:')
			if key == '':
				self.think_it_out()
			elif key == 'i':
				self.input_incoming()
			elif key == 'q':
				print('\nq pressed, exiting...\n')
				return False

			# print all config
			self.print_all()

			self.propagate()
		else:
			print('Wait till processing is complete!')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

if __name__ == '__main__':
	n_nodes = 5
	n_input_nodes = 1
	n_feedbacks = 1
	n_outputs = 1
	# n_input_nodes = max(2, randint(0, int(n_nodes*.2)))
	# n_feedbacks = max(1, randint(0, int(n_nodes*.1)))
	# n_outputs = max(1, randint(0, int(n_nodes*.1)))

	combi = list(combinations(range(n_nodes), 2))
	sampled = sample(combi, randint(int(len(combi)*.5), int(len(combi)*.5)))

	# pack_sampler = lambda: list(np.random.randint(0, 9, 255))
	# pack_sampler = lambda: [randint(0,9)]
	pack_sampler = lambda: randint(0,9)
	input_nodes = sample(range(n_nodes),
						 n_input_nodes)
	feedbacks = sample(list(set(range(n_nodes)) - set(input_nodes)),
					   n_feedbacks)
	outputs = sample(list(set(range(n_nodes)) - set(input_nodes) - set(feedbacks)),
					 n_outputs)

	input_vals = list(map(lambda x:[x], list(range(10))))

	config = dotdict({
		'n_nodes': n_nodes,
		'pack_init': pack_sampler,
		'edges_init': sampled,
		'inputs': input_nodes,
		'feedbacks': feedbacks,
		'outputs': outputs,
		'input_vals': input_vals
	})
	one = Mind(config)
	# think()

	print(
		'1. Press Enter to process data''\n'
		'2. Enter i to take in input''\n'
		'3. Enter q to exit''\n'
	)

	# with Listener(on_press=one.propagate) as listener:
	# 	listener.join()
	one.propagate()
