import page_rank
import numpy

"""
Created a test file from the example on the slides and named it PageRank_00.txt
"""
TEST_FILE_NUMBER = 0


class TestPageRank(numpy.testing.TestCase):
    graph = page_rank.Graph()

    def setUp(self):
        self.graph = page_rank.Graph()
        self.graph.create_graph_from_file(TEST_FILE_NUMBER)

    def test_h_matrix(self):
        """
        Test the H matrix against the example from the slides
        """
        matrix = numpy.matrix([
            [0.0, 1.0 / 2.0, 1.0 / 2.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0 / 3.0, 1.0 / 3.0, 0.0, 0.0, 1.0 / 3.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0 / 2.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 2.0, 0.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 1.0, 0.0, 0.0]
        ], numpy.float64)
        self.graph.create_h_matrix()
        numpy.testing.assert_allclose(self.graph.h_matrix, matrix, rtol=1e-15, atol=1e-15)

    def test_s_matrix(self):
        """
        Test the S matrix against the example from the slides
        """
        matrix = numpy.matrix([
            [0.0, 1.0 / 2.0, 1.0 / 2.0, 0.0, 0.0, 0.0],
            [1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0],
            [1.0 / 3.0, 1.0 / 3.0, 0.0, 0.0, 1.0 / 3.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0 / 2.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 2.0, 0.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 1.0, 0.0, 0.0]
        ], numpy.float64)
        self.graph.create_h_matrix()
        self.graph.create_s_matrix()
        numpy.testing.assert_allclose(self.graph.s_matrix, matrix, rtol=1e-15, atol=1e-15)

    def test_g_matrix(self):
        """
        Test the G matrix against the example from the slides
        """
        matrix = numpy.matrix([
            [1.0 / 60.0, 7.0 / 15.0, 7.0 / 15.0, 1.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0],
            [1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0],
            [19.0 / 60.0, 19.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0, 19.0 / 60.0, 1.0 / 60.0],
            [1.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0, 7.0 / 15.0, 7.0 / 15.0],
            [1.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0, 7.0 / 15.0, 1.0 / 60.0, 7.0 / 15.0],
            [1.0 / 60.0, 1.0 / 60.0, 1.0 / 60.0, 11.0 / 12.0, 1.0 / 60.0, 1.0 / 60.0]
        ], numpy.float64)
        self.graph.create_h_matrix()
        self.graph.create_s_matrix()
        self.graph.create_g_matrix(damping_factor=0.9)
        numpy.testing.assert_allclose(self.graph.g_matrix, matrix, rtol=1e-15, atol=1e-15)
