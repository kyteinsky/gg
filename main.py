from graph import Graph, dotdict

from itertools import combinations
from random import sample, randint
import numpy as np

from pprint import pprint


class Mind(Graph):

	def __init__(self, kwargs):
		super().__init__(kwargs)
		# for k, v in self.roles.items():
		# 	print(k)
		# 	for i in v:
		# 		pprint(print(i))
		# 	print('-------------------------')
		
		# init output and feedback to zero
		for o, f in zip(self.roles.output, self.roles.feedback):
			o.pack = 0
			f.pack = 0
		
		self.print_all()
		# print(self.roles.values())


	def input_incoming(self, input_set):
		# get input, set it to input node pack
		if not len(input_nodes) == len(self.roles.input):
			raise ValueError(f'Length of input pack list is not correct, should be {len(input_nodes)}, was found to be {len(self.roles.input)}')
		
		for input_node, val in zip(self.roles.input, input_set):
			# input_node.pack = [val]
			input_node.pack = val
		
		self.think_it_out()


	def think_it_out(self):
		# OVERFLOW RULE
		# all nodes except input nodes
		for node_set in self.roles.values():
			if node_set[0].role == 'input': continue
			print('role:',node_set[0].role)

			for node in node_set:
				print(f'---node:{node.id}')
				if node.pack > 9:
					overflow = node - 9
					print(f'overflow:{overflow}')

					# update connected nodes
					for edge in node.edges:
						print(f'edge:{edge.id}, ends:{edge.ends}')
						self.nodes[edge.ends[(0,1)[edge.ends[0] == node.id]]].pack += overflow


	def propagate(self, input_set): # BFS
		try: 
			if input('press key to propagate once ') == 'i':
				self.input_incoming(input_set)
			else:
				self.think_it_out()
		
		except KeyboardInterrupt: 
			print('\nCtrl+C pressed, exiting...\n')
			quit()

		# print all config
		self.print_all()

		self


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

	config = dotdict({
		'n_nodes': n_nodes,
		'pack_init': pack_sampler,
		'edges_init': sampled,
		'inputs': input_nodes,
		'feedbacks': feedbacks,
		'outputs': outputs
	})
	one = Mind(config)
	# think()

	input_vals = list(map(lambda x:[x], list(range(10))))
	# input_vals = list(range(10))

	for i in input_vals:
		one.propagate(i)
