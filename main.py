from graph import Graph, dotdict

from itertools import combinations
from random import sample, randint
import numpy as np

from pprint import pprint


class Think(Graph):

	def __init__(self, kwargs):
		super().__init__(kwargs)
		# for k, v in self.roles.items():
		# 	print(k)
		# 	for i in v:
		# 		pprint(print(i))
		# 	print('-------------------------')
		

	def propagate(self, input_vals:list):
		input('press key to propagate once') # BFS

		# get input, set it to input node pack
		if not len(input_nodes) == len(self.roles.input):
			raise ValueError(f'Length of input pack list is not correct, should be {len(input_nodes)}, was found to be {len(self.roles.input)}')

		for input_node in self.roles.input:
			input_node.


if __name__ == '__main__':
	n_nodes = 20
	n_input_nodes = max(2, randint(0, int(n_nodes*.2)))
	n_feedbacks = max(1, randint(0, int(n_nodes*.1)))
	n_outputs = max(1, randint(0, int(n_nodes*.1)))

	combi = list(combinations(range(n_nodes), 2))
	sampled = sample(combi, randint(int(len(combi)*.5), int(len(combi)*.5)))

	# pack_sampler = lambda: list(np.random.randint(0, 9, 255))
	pack_sampler = lambda: [randint(0,9)]
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
	think = Think(config)
	think()

