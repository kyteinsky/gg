
import torch.empty as empty_tensor

class Graph:

    def __init__(self, n_nodes, pack_size):
        self.nodes = []
        self.edge_ord = 0

        self.pack_size = pack_size
        if not self.pack_size: self.pack_size = 4
        for _id in range(n_nodes):
            node = Node(_id, self.pack_size)
            self.nodes.append(node)

    def add_edge(self, _id_one, _id_two):
        """
        one: id of first node
        two: id of second node
        First and second terminology holds no significance as such
        in an undirected graph as this
        """
        edge = Edge(self.edge_ord, _id_one, _id_two)
        self.nodes[_id_one].edges().append(edge)
        self.nodes[_id_two].edges().append(edge)

    def add_node(self):
        """
        Just append one node to the nodes list
        """
        node = Node(len(self.nodes), self.pack_size)
        self.nodes.append(node)
    
    def __call__(self, **):
        pass



class Node:

    def __init__(self, _id, pack_size):
        self.node = dict()
        self.node["id"] = _id
        self.node["pack"] = empty_tensor(pack_size)
        self.node["edges"] = []

    def get_id(self):
        return self.node["id"]
    
    def pack(self):
        return self.node["pack"]

    def edges(self):
        return self.node["edges"]


class Edge:

    def __init__(self, _id, _id_one, _id_two):
        self.edge = dict()
        self.edge["id"] = _id
        self.edge["ends"] = [_id_one, _id_two]
    
    def get_id(self):
        return self.edge['id']
    
    def ends(self):
        return self.edge['ends']

