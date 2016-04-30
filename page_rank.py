"""
Final Project - Page Rank Algorithm
Michael Palmer
CSCI 5330 A
May 4, 2016
"""
import re
import numpy as np
import numpy.matlib as ml
# from collections import OrderedDict

# Path to the directory containing test files
import operator

from objc._objc import super

DATA_DIR = './page_rank_data'


class Node:
    """
    Node
    """
    def __init__(self, name):
        """
        Create a new Node
        :param name: Node name
        :type name: str
        """
        self.name = name

    def __str__(self):
        return self.name


class Edge:
    """
    Edge
    """
    def __init__(self, node_from, node_to, directed=True):
        """
        Create a new Edge
        :param node_from: Node from
        :type node_from: Node
        :param node_to: Node to
        :type node_to: Node
        :param directed: Is this a directed edge?
        :type directed: bool
        """
        self.node_from = node_from
        self.node_to = node_to
        self.directed = directed

    def __str__(self):
        return '%s -> %s (%sdirected)' % (self.node_from.name, self.node_to.name, 'un' if not self.directed else '')


class Set(list):
    """
    Set
    """
    model = str

    def add(self, *args, **kwargs):
        """
        Add an item to the set
        """
        item = self.model(*args, **kwargs)
        if item in self:
            raise Exception('Item "%s" already exists' % item)
        self.append(item)

    def remove(self, item):
        """
        Remove an item from the set
        :param item: Item to remove
        """
        super(Set, self).remove(self.get(item))

    def find(self, item):
        """
        Does the specified object exist in the set?
        :param item: Item to search for
        :type item: str|object
        :return: true or false
        :rtype: bool
        """
        return item in self

    def get(self, name):
        """
        Return the object identified by the specified name
        :param name: Item identifier
        :type name: str
        :return: Item
        :rtype: self.model
        """
        if not self.find(name):
            raise ValueError('Item "%s" does not exist' % name)
        for element in self:
            if str(element) == name:
                return element

    def get_index(self, item):
        """
        Get the index of the specified item
        :param item:
        :return: index of the item
        :rtype: int
        """
        if not self.find(item):
            raise ValueError('Item "%s" does not exist' % item)
        for i, element in enumerate(self):
            if str(element) == str(item):
                return i

    def describe(self):
        """
        Return a string representation of the items in the set
        :return: item in set
        :rtype: str
        """
        return str(self)

    def __contains__(self, item):
        return str(item) in [str(element) for element in self]

    def __str__(self):
        return ', '.join([str(item) for item in self])


class NodeSet(Set):
    model = Node


class EdgeSet(Set):
    model = Edge


class Graph:
    """
    Graph
    """
    def __init__(self, name='Graph'):
        """
        Create a new instance of a Graph
        :param name: Graph name
        """
        self.name = name
        self.node_set = NodeSet()
        self.edge_set = EdgeSet()
        # h_matrix = OrderedDict()
        self.h_matrix = ml.matrix([0], dtype=np.float64)
        # s_matrix = OrderedDict()
        self.s_matrix = ml.matrix([0], dtype=np.float64)
        # g_matrix = OrderedDict()
        self.g_matrix = ml.matrix([0], dtype=np.float64)
        # self.pi_vector = OrderedDict()
        self.pi_vector = ml.matrix([0], dtype=np.float64)

    def create_graph_from_file(self, file_num):
        """
        Fill node and edge sets from an input file
        :param file_num: File number
        :type file_num: int
        """
        with open(DATA_DIR + '/PageRank_0%d.txt' % file_num) as f:
            for line in f:
                matches = re.search(r'^(Node|Edge)Name = ([a-zA-Z]\d+)(?:->([a-zA-Z]\d+))?$', line)
                if matches:
                    if matches.group(1) == 'Node':
                        self.node_set.add(matches.group(2))
                    else:
                        node_from = self.node_set.get(matches.group(2))
                        node_to = self.node_set.get(matches.group(3))
                        self.edge_set.add(node_from, node_to)

    def create_h_matrix(self):
        """
        Create a transition matrix from the nodes and edges
        """
        self.h_matrix = ml.zeros((len(self.node_set), len(self.node_set)), dtype=np.float64)
        for i, node in enumerate(self.node_set):
            # print(node.name)
            # print([edge.node_to.name for edge in self.edge_set if edge.node_from.name == node.name])
            out_links = [self.node_set.get_index(edge.node_to.name)
                         for edge in self.edge_set if edge.node_from.name == node.name]
            for j in out_links:
                self.h_matrix[i, j] = 1.0/len(out_links)

        # h_matrix = OrderedDict()
        # for node in self.node_set:
        #     h_matrix[node.name] = OrderedDict()
        #     for node2 in self.node_set:
        #         h_matrix[node.name][node2.name] = 0
        #
        # out_links = {}
        # for node in self.node_set:
        #     out_links[node.name] = [edge.node_to.name for edge in self.edge_set if edge.node_from.name == node.name]
        #     print(node.name, out_links[node.name])
        #     for item in out_links[node.name]:
        #         items = float(len(out_links[node.name]))
        #         h_matrix[node.name][item] = 1 / items
        # print('H MATRIX')
        # self.describe_matrix(h_matrix)

    def create_s_matrix(self):
        """
        Create a Stochastic matrix from the H matrix
        S = H + a(1/n * eT )
        """
        self.s_matrix = self.h_matrix.copy()
        for a in self.s_matrix:
            a += 1.0/len(self.node_set) * (not a.sum())

        # self.s_matrix = self.h_matrix
        # for a, b in self.s_matrix.items():
        #     dangling = True
        #     for c, d in b.items():
        #         if d != 0:
        #             dangling = False
        #             break
        #     if dangling:
        #         self.s_matrix[a] = OrderedDict()
        #         for key, value in self.s_matrix.items():
        #             self.s_matrix[a][key] = 1/float(len(self.s_matrix))
        # print('\nS MATRIX')
        # self.describe_matrix(self.s_matrix)

    def create_g_matrix(self, damping_factor=0.9):
        """
        Create the Google matrix from the S matrix
        G = alpha * H + (alpha * a + (1 - alpha) e) 1/n * e^T
        :param damping_factor: Damping factor (default is 0.9)
        :type damping_factor: float
        """
        self.g_matrix = damping_factor * self.s_matrix + (1.0 - damping_factor) * (1.0 / len(self.node_set))

    def compute_page_rank(self):
        """
        Compute the page rank
        """
        self.pi_vector = ml.matrix([1.0/len(self.node_set)] * len(self.node_set), np.float64)
        for _ in range(self.g_matrix.size):
            self.pi_vector *= self.g_matrix
        # Round to 4 decimal places
        self.pi_vector = np.around(self.pi_vector, 4)
        rank = {self.node_set[i].name: x for i, x in enumerate(self.pi_vector[0])}
        sorted_rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
        for i, item in enumerate(sorted_rank):
            print('Rank #%d: %s' % (i+1, item[0]))

    def describe_graph(self):
        """
        Print details about this graph
        """
        for node in self.node_set:
            in_links = [edge.node_from.name for edge in self.edge_set if edge.node_to.name == node.name]
            out_links = [edge.node_to.name for edge in self.edge_set if edge.node_from.name == node.name]
            print('Node %s' % node.name)
            print('Links in:  %s' % in_links)
            print('Links out: %s\n' % out_links)

    def describe_matrix(self, matrix):
        """
        Print a matrix
        :param matrix: Matrix to output
        :type matrix: numpy.matlib.matrix
        """
        print('\t\t' + ('\t\t\t'.join([node.name for node in self.node_set])))
        for i, row in enumerate(matrix):
            data = [self.node_set[i].name]
            for j in range(row.size):
                b = matrix[i, j]
                data.append(('%d      ' if int(b) == b else '%.5f') % b)
            print('\t\t'.join(data))

        # print('\t\t' + ('\t\t\t'.join(matrix.keys())))
        # for k, v in matrix.items():
        #     row = [k]
        #     for a, b in v.items():
        #         row.append(('%d   ' if int(b) == b else '%.2f') % b)
        #     print('\t\t'.join(row))


class Main:
    """
    Main class
    """
    __graph = Graph()

    @staticmethod
    def create_graph_from_file(file_num):
        Main.__graph.create_graph_from_file(file_num)
        print('### Graph Description ###')
        print('-' * 75)
        print(Main.__graph.node_set.describe())
        print(Main.__graph.edge_set.describe())

        # Create the matrices
        Main.__graph.create_h_matrix()
        Main.__graph.create_s_matrix()
        Main.__graph.create_g_matrix(damping_factor=0.9)

        print('\n### Transition Matrix (H) ###')
        print('-' * 75)
        Main.__graph.describe_matrix(Main.__graph.h_matrix)

        print('\n### Stochastic Matrix (S) ###')
        print('-' * 75)
        Main.__graph.describe_matrix(Main.__graph.s_matrix)

        print('\n### Google Matrix (G) ###')
        print('-' * 75)
        Main.__graph.describe_matrix(Main.__graph.g_matrix)

        print('\n### Page Rankings ###')
        print('-' * 75)
        Main.__graph.compute_page_rank()

    @staticmethod
    def print_graph():
        """
        Generate a visual graph using NetworkX and PyLab
        """
        import networkx as nx
        import pylab

        graph = nx.DiGraph()
        for edge in Main.__graph.edge_set:
            graph.add_edge(edge.node_from.name, edge.node_to.name)

        pos = nx.shell_layout(graph)
        nx.draw(graph, pos, node_size=1500, node_color='yellow', edge_color='red', with_labels=True)
        pylab.show()

if __name__ == '__main__':
    Main.create_graph_from_file(0)  # int(input('Enter file number [1 - 5]: ')))
    Main.print_graph()
