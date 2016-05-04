#!/usr/bin/env python2.7
"""
Algorithm Final Project - Google's page rank algorithm
Michael Palmer
CSCI 5330 A
May 4, 2016

Program Summary:
----------------
The purpose of this program is to create an implementation of Google's page rank algorithm.
Important web pages typically have a large number of other web pages that link to it. The
algorithm follows that logic and calculates the importance of a web page based on the number
of pages that link to it. This value is then divided by the total number of pages to get a
probability of moving from one page to another.

Important Notes:
----------------
In writing this program, the test files were placed in ./page_rank_data. If your test files
are located in another directory, modify DATA_DIR with the appropriate path.

The NetworkX and PyLab libraries are required to display the optional visualization of the
graph. It can be disabled (i.e. if the library does not work on your machine) by setting
GRAPH_VISUALIZATION to False.

Test file 0 is the example illustrated in the slides.

Python version: 2.7
"""
import re
import numpy as np
import numpy.matlib as ml
from operator import itemgetter
from os import environ

# Path to the directory containing test files
DATA_DIR = './page_rank_data'

# Create a visualization of the graph (requires NetworkX and PyLab)
GRAPH_VISUALIZATION = True

# Assigned test file number
ASSIGNED_FILE_NO = 5

# Running in PyCharm? (When run in terminal, tabs show differently)
PYCHARM = environ.get('PYCHARM_HOSTED', 0) == '1'


class Node:
    """
    Node class
    """
    def __init__(self, name):
        """
        Create a new Node
        :param name: Node name
        :type name: str
        """
        self.name = name

    def __str__(self):
        """
        Create string description of this Node
        :return: Node name
        """
        return self.name


class Edge:
    """
    Edge class
    """
    def __init__(self, node_from, node_to, directed=True):
        """
        Create a new Edge
        :param node_from: Node from
        :param node_to: Node to
        :param directed: Is this a directed edge? (default is True)
        :type node_from: Node
        :type node_to: Node
        :type directed: bool
        """
        self.node_from = node_from
        self.node_to = node_to
        self.directed = directed

    def __str__(self):
        """
        Create string description of this Edge
        :return: Edge description
        """
        return '%s %s %s' % (self.node_from.name, '->' if self.directed else '+', self.node_to.name)


class Set(list):
    """
    Set class
    """
    # Element model
    model = str

    def add(self, *args, **kwargs):
        """
        Add an item to the set
        """
        # Create new instance of the element model, passing in arguments
        item = self.model(*args, **kwargs)

        # Verify item does not exist yet
        if item in self:
            raise Exception('Item "%s" already exists' % item)

        # Add it
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
        :type item: object
        :return: True or False
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
        # Check if it exists
        if not self.find(name):
            raise ValueError('Item "%s" does not exist' % name)

        # Get the object
        for element in self:
            if str(element) == name:
                return element

    def get_index(self, item):
        """
        Get the index of the specified item
        :param item:
        :type item: object
        :return: index of the item
        :rtype: int
        """
        # Check if it exists
        if not self.find(item):
            raise ValueError('Item "%s" does not exist' % item)

        # Get the index
        for i, element in enumerate(self):
            if str(element) == str(item):
                return i

    def describe(self):
        """
        Print a string representation of the items in the set
        """
        print(self)

    def __contains__(self, item):
        """
        Check if the item exists in this set
        :param item: Item to compare
        :return: True|False
        """
        return str(item) in [str(element) for element in self]

    def __str__(self):
        """
        Create string representation of all items in the set
        :return: String of items in set
        """
        return ', '.join([str(item) for item in self])


class NodeSet(Set):
    """
    Node Set - a list of Nodes
    """
    # Override the model used by the Set
    model = Node


class EdgeSet(Set):
    """
    Edge Set - a list of Edges
    """
    # Override the model used by the Set
    model = Edge


class Graph:
    """
    Graph - Performs computations to calculate matrices and page ranking based on a set of nodes and edges
    """
    def __init__(self, name='Graph'):
        """
        Create a new Graph
        :param name: Graph name
        :type name: str
        """
        self.name = name
        self.node_set = NodeSet()
        self.edge_set = EdgeSet()
        self.h_matrix = ml.matrix([0], dtype=np.float64)
        self.s_matrix = ml.matrix([0], dtype=np.float64)
        self.g_matrix = ml.matrix([0], dtype=np.float64)
        self.pi_vector = ml.matrix([0], dtype=np.float64)
        self.rankings = []

    def create_graph_from_file(self, file_no):
        """
        Fill node and edge sets from an input file
        :param file_no: File number
        :type file_no: int
        """
        # Open the test file
        with open(DATA_DIR + '/PageRank_%.2d.txt' % file_no) as f:
            # Loop through each line
            for line in f:
                # Search for matching data
                matches = re.search(r'^(Node|Edge)Name = ([a-zA-Z]\d+)(?:->([a-zA-Z]\d+))?$', line)
                if matches:
                    if matches.group(1) == 'Node':
                        # Add node
                        self.node_set.add(matches.group(2))
                    else:
                        # Add edge
                        node_from = self.node_set.get(matches.group(2))
                        node_to = self.node_set.get(matches.group(3))
                        self.edge_set.add(node_from, node_to)

    def create_h_matrix(self):
        """
        Create adjacency matrix from the nodes and edges
        """
        # Initialize the matrix with zeros
        self.h_matrix = ml.zeros((len(self.node_set), len(self.node_set)), dtype=np.float64)

        # Loop through the nodes
        for i, node in enumerate(self.node_set):
            # Find all nodes that this one links to
            out_links = [self.node_set.get_index(edge.node_to.name)
                         for edge in self.edge_set if edge.node_from.name == node.name]

            # Update the matrix
            for j in out_links:
                self.h_matrix[i, j] = 1.0/len(out_links)

    def create_s_matrix(self):
        """
        Create transition Stochastic matrix from the H matrix
        S = H + a(1/n * eT )
        """
        # Copy the H matrix
        self.s_matrix = self.h_matrix.copy()

        # Set all dangling nodes to 1/N
        for a in self.s_matrix:
            a += 1.0/len(self.node_set) * (not a.sum())

    def create_g_matrix(self, damping_factor=0.85):
        """
        Create Google matrix from the S matrix
        Formula: G = damping_factor * S + (1 - damping_factor) * 1/N
        :param damping_factor: Damping factor (default is 0.85)
        :type damping_factor: float
        """
        self.g_matrix = damping_factor * self.s_matrix + (1.0 - damping_factor) * 1.0 / len(self.node_set)

    def create_pi_vector(self):
        """
        Create the Pi Vector from the G matrix
        """
        # Initialize the matrix to be [[1/N, 1/N, ..., 1/N]]
        self.pi_vector = ml.matrix([1.0 / len(self.node_set)] * len(self.node_set), np.float64)

        # Multiply the Pi vector and G matrix together until values have converged (iterations = cols * rows)
        for _ in range(self.g_matrix.size):
            self.pi_vector *= self.g_matrix

    def compute_page_rank(self):
        """
        Compute the page rank from the Pi vector
        """
        # Iterate through the Pi vector and connect the node name to its vector value
        ranks = {self.node_set[i].name: np.float(value) for i, value in enumerate(np.nditer(self.pi_vector))}

        # Sort the rankings by the vector value in descending order
        sorted_ranks = sorted(ranks.items(), key=itemgetter(1), reverse=True)

        # Save the ranking order (for the unit test)
        self.rankings = [node[0] for node in sorted_ranks]

        # Output the rankings, in order, with their vector values
        for i, (node, rank) in enumerate(sorted_ranks):
            print('Rank #%d: %s (%.5f)' % (i+1, node, rank))

    def describe_graph(self):
        """
        Print details about this graph
        """
        for node in self.node_set:
            # Compile in-links and out-links
            in_links = [edge.node_from.name for edge in self.edge_set if edge.node_to.name == node.name]
            out_links = [edge.node_to.name for edge in self.edge_set if edge.node_from.name == node.name]

            # Output results
            print('Node %s' % node.name)
            print('Links in:  %s' % (', '.join(in_links) if len(in_links) else 'None'))
            print('Links out: %s\n' % (', '.join(out_links) if len(out_links) else 'None'))

    def describe_matrix(self, matrix, row_labels=True):
        """
        Print a matrix
        :param matrix: Matrix to output
        :param row_labels: Print the row labels? (default is True)
        :type matrix: numpy.matlib.matrix
        :type row_labels: bool
        """
        # Set number of tabs based on if running in PyCharm or not
        tabs = '\t\t\t' if PYCHARM else '\t\t'

        # Column headers
        print('\t\t' + (tabs.join([node.name for node in self.node_set])))

        # Loop through the matrix rows
        for i, row in enumerate(matrix):
            # Row header
            output = [self.node_set[i].name] if row_labels else ['']

            # Loop through the matrix columns
            for j in range(row.size):
                value = matrix[i, j]

                # Add value to output
                output.append(('%d      ' if int(value) == value else '%.5f') % value)

            # Print the row output
            print('\t\t'.join(output))


class Main:
    """
    Main - Runs test cases
    """
    __graph = Graph()
    __file_num = 0

    @staticmethod
    def create_graph_from_file():
        """
        Create a graph using data from a test file
        """
        # Test file number input
        print('Press enter to use the assigned test file (%.2d) or enter a custom file number.' % ASSIGNED_FILE_NO)
        input_file = raw_input('Enter test file number [0 - 5]: [%.2d] ' % ASSIGNED_FILE_NO)
        Main.__file_num = ASSIGNED_FILE_NO if input_file == '' else int(input_file)

        # Create the graph from the test file
        Main.__graph.create_graph_from_file(Main.__file_num)

        # Generate the matrices
        Main.__graph.create_h_matrix()
        Main.__graph.create_s_matrix()
        Main.__graph.create_g_matrix(damping_factor=0.9)
        Main.__graph.create_pi_vector()

    @staticmethod
    def print_graph():
        """
        Generate output
        """
        divider_length = 13 if PYCHARM else 18

        # Header
        print('\nCSCI 5330 Spring 2016')
        print('Michael Palmer')
        print('900757121')

        # Details about the input file
        print('\nInput')
        print('-' * divider_length * len(Main.__graph.node_set))
        print('Graph Number: %.2d' % Main.__file_num)
        print('\nNodes:')
        Main.__graph.node_set.describe()
        print('\nEdges:')
        Main.__graph.edge_set.describe()

        # Adjacency matrix
        print('\nAdjacency Matrix (H)')
        print('-' * divider_length * len(Main.__graph.node_set))
        Main.__graph.describe_matrix(Main.__graph.h_matrix)

        # Stochastic matrix
        print('\nStochastic Matrix (S)')
        print('-' * divider_length * len(Main.__graph.node_set))
        Main.__graph.describe_matrix(Main.__graph.s_matrix)

        # Google matrix
        print('\nGoogle Matrix (G)')
        print('-' * divider_length * len(Main.__graph.node_set))
        Main.__graph.describe_matrix(Main.__graph.g_matrix)

        # Pi vector
        print('\nPi Vector')
        print('-' * divider_length * len(Main.__graph.node_set))
        Main.__graph.describe_matrix(Main.__graph.pi_vector, False)

        # Page rankings
        print('\nPage Rankings')
        print('-' * divider_length * len(Main.__graph.node_set))
        Main.__graph.compute_page_rank()

        # If enabled, display the visualization
        if GRAPH_VISUALIZATION:
            import networkx as nx
            import pylab

            # Initialize the graph
            graph = nx.DiGraph()

            # Add edges
            for edge in Main.__graph.edge_set:
                graph.add_edge(edge.node_from.name, edge.node_to.name)

            # Set layout, draw the graph, and display it
            pos = nx.shell_layout(graph)
            nx.draw(graph, pos, node_size=1500, node_color='yellow', edge_color='red', with_labels=True)
            pylab.show()

if __name__ == '__main__':
    # Run the test cases and print the results
    Main.create_graph_from_file()
    Main.print_graph()
