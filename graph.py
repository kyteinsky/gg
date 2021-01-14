
from itertools import combinations
from random import sample, randint
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, kwargs):
        self.roles = dotdict({
            'gen': [],
            'input': [],
            'output': [],
            'feedback': [],
        })  # storage for all nodes, classified

        self.nodes = []
        self.edge_ord = 0
        self.pack = kwargs.pack_init  # function to sample from
        self.edges_init = kwargs.edges_init
        self.input_vals = kwargs.input_vals

        # self.pack_size = pack_size
        # if not self.pack_size: self.pack_size = 4
        for _id in range(kwargs.n_nodes):
            node = Node(_id, self.pack)
            self.nodes.append(node)

        for (_id_one, id_two) in self.edges_init:
            self.add_edge(_id_one, id_two)

        # assign roles
        self.set_roles(kwargs.inputs, 'input')
        self.set_roles(kwargs.feedbacks, 'feedback')
        self.set_roles(kwargs.outputs, 'output')
        self.set_roles(list(
            set(range(kwargs.n_nodes)) 
            - set(kwargs.feedbacks) 
            - set(kwargs.inputs) 
            - set(kwargs.outputs)
        ), 'gen')

        self.outputs = dict()
        # record outputs
        for output_node in kwargs.outputs:
            self.outputs[self.nodes[output_node].id] = []


    def add_edge(self, _id_one, _id_two):
        """
        First and second terminology holds no significance 
        as such in an undirected graph as this
        """
        edge = Edge(self.edge_ord, _id_one, _id_two)
        self.nodes[_id_one].edges.append(edge)
        self.nodes[_id_two].edges.append(edge)
        self.edge_ord += 1

    def add_node(self):
        """
        Just append one node to the nodes list
        """
        node = Node(len(self.nodes), self.pack)
        self.nodes.append(node)

    def set_roles(self, ids, role):
        for i in ids:
            self.nodes[i].role = role
            self.roles[role].append(self.nodes[i])

    @staticmethod
    def color_map(for_what):
        return {
            'gen': 'blue',
            'input': 'crimson',
            'output': 'green',
            'feedback': 'yellow'
        }[for_what]

    def print_all(self):
        # for i in self.nodes:
        #     print(
        #         f'Node: {i.id},\trole: {i.role},\tpack: {i.pack},\tedges: {[e.id for e in i.edges]}')
        
        for role in self.roles.values():
            for i in role:
                print(
                # f'Node: {i.id},\trole: {i.role},\tpack: {i.pack},\tedges: {[e.id for e in i.edges]}')
                f'Node: {i.id},''\t'
                f'role: {i.role},''\t'
                f'pack: {i.pack},''\t'
                f'edges: {len(i.edges)}')
    

    def __call__(self):
        G = nx.Graph()
        G.add_nodes_from([i.id for i in self.nodes])
        G.add_edges_from(self.edges_init)
        color_map = []

        for i in G.nodes:
            color_map.append(self.color_map(self.nodes[i].role))

        # plotting
        # nx.draw_networkx(G)
        nx.draw(G, node_color=color_map, with_labels=True)
        plt.show()

    def __str__(self):
        return f'Graph with {len(self.nodes)} nodes.'


class Node:
    def __init__(self, _id, pack, role='gen'):
        self.id = _id
        self.pack = pack()
        self.edges = []
        self.role = role

    def __str__(self):
        return f'Node: {self.id},\trole: {self.role},\tpack: {self.pack},\tedges: {[e.desc for e in self.edges]}'

    @property
    def desc(self):
        return self.__str__()


class Edge:
    def __init__(self, _id, _id_one, _id_two):
        self.id = _id
        self.ends = [_id_one, _id_two]

    def __str__(self):
        return f'Edge: {self.id}, Ends: {self.ends}'

    @property
    def desc(self):
        return self.__str__()


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# if __name__ == "__main__":
#     # n_nodes = max(10, 20)
#     n_nodes = 5
#     combi = list(combinations(range(n_nodes), 2))
#     sampled = sample(combi, randint(int(len(combi)*.5), int(len(combi)*.5)))
#     # sampled = sample(combi, len(combi)//2)
#     pack_sampler = lambda: randint(0, 9)
#     input_nodes = sample(range(n_nodes),
#                          max(2, randint(0, int(n_nodes*.2))))
#     feedbacks = sample(list(set(range(n_nodes)) - set(input_nodes)),
#                        max(1, randint(0, int(n_nodes*.1))))
#     outputs = sample(list(set(range(n_nodes)) - set(input_nodes) - set(feedbacks)),
#                      max(1, randint(0, int(n_nodes*.1))))

#     config = dotdict({
#         'n_nodes': n_nodes,
#         'pack_init': pack_sampler,
#         'edges_init': sampled,
#         'inputs': input_nodes,
#         'feedbacks': feedbacks,
#         'outputs': outputs
#     })

#     graph = Graph(config)
#     graph()
