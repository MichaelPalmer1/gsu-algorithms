from abc import ABCMeta
import re
import numpy as np
import numpy.matlib as ml
# from collections import OrderedDict

DATA_DIR = './page_rank_data'

# class Set:
#     def add(self, item):
#         if item in self.data:
#             raise Exception('Item "%s" already exists' % item)
#         self.data.append(item)
#
#     def remove(self, item):
#         if item in self.data:
#             raise Exception('Item "%s" does not exist' % item)
#         self.data.remove(item)
#
#     def get(self, item):
#         """
#         Return the specified object
#         :param index:
#         :return: object
#         """
#         return self.data[item]
#
#     def describe(self):
#         return self.data


class Node:
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
    model = ABCMeta

    def add(self, *args, **kwargs):
        """
        Add a new item to the set
        :param args:
        :param kwargs:
        :return:
        """
        self.append(self.model(*args, **kwargs))

    def find(self, item):
        """
        Does the specified object exist in the set?
        :param item: Item to search for
        :type item: str|object
        :return: true or false
        :rtype: bool
        """
        return self.get(item) is not None

    def get(self, item):
        """
        Return the specified object
        :param item:
        :return:
        """
        for x in self:
            if x.name == item:
                return x
        return None

    def get_index(self, item):
        """
        Get the index of the specified item
        :param item:
        :return: index
        :rtype: int
        """
        for n, x in enumerate(self):
            if x.name == item:
                return n
        return None

    def describe(self):
        """
        Return a list representation of the items in the set
        :return: list of items
        :rtype: list
        """
        # return [item for item in self]
        return str(self)

    def __str__(self):
        return ', '.join([str(item) for item in self])


class NodeSet(Set):
    model = Node
    # def add(self, item):
    #     node = Node(item)
    #     self.append(node)


class EdgeSet(Set):
    model = Edge
    # def add(self, item, node_from, node_to, directed=True):
    #     edge = Edge(item, node_from, node_to, directed)
    #     self.append(edge)
    #
    # def describe(self):
    #     items = []
    #     for item in self:
    #         items.append('%s -> %s' % (item.node_from.name, item.node_to.name))
    #     return items


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
        """
        self.g_matrix = damping_factor * self.s_matrix + (1.0 - damping_factor) * 1.0 / len(self.node_set)

    def compute_page_rank(self):
        pass

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
    def __init__(self):
        self.__graph = Graph()

    def create_graph_from_file(self, file_num):
        self.__graph.create_graph_from_file(file_num)
        print(self.__graph.node_set.describe())
        print(self.__graph.edge_set.describe())
        self.__graph.create_h_matrix()
        self.__graph.create_s_matrix()
        self.__graph.create_g_matrix(damping_factor=0.9)
        self.__graph.describe_matrix(self.__graph.h_matrix)
        print('----------')
        self.__graph.describe_matrix(self.__graph.s_matrix)
        print('----------')
        self.__graph.describe_matrix(self.__graph.g_matrix)

    def print_graph(self):
        import networkx as nx
        import pylab

        graph = nx.DiGraph()
        for edge in self.__graph.edge_set:
            graph.add_edge(edge.node_from.name, edge.node_to.name, weight=0)

        pos = nx.shell_layout(graph)
        nx.draw(graph, pos, node_size=1500, node_color='yellow', edge_color='red', with_labels=True)
        pylab.show()


if __name__ == '__main__':
    m = Main()
    m.create_graph_from_file(0)  # int(input('Enter file number [1 - 5]: ')))
    # m.print_graph()
