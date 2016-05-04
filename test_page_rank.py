import page_rank
import numpy

"""
Created a test file from the example on the slides and named it PageRank_00.txt.
"""
TEST_FILE_NUMBER = 0


class TestPageRank(numpy.testing.TestCase):
    graph = page_rank.Graph()

    def setUp(self):
        self.graph = page_rank.Graph()
        self.graph.create_graph_from_file(TEST_FILE_NUMBER)
        print(self._testMethodDoc)

    def test_h_matrix(self):
        """
        Test the H matrix against the example from the slides
        """
        expected = numpy.matrix([
            [0.0, 1.0 / 2.0, 1.0 / 2.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0 / 3.0, 1.0 / 3.0, 0.0, 0.0, 1.0 / 3.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0 / 2.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 2.0, 0.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 1.0, 0.0, 0.0]
        ], numpy.float64)
        self.graph.create_h_matrix()
        self.graph.describe_matrix(self.graph.h_matrix)
        numpy.testing.assert_allclose(self.graph.h_matrix, expected)

    def test_s_matrix(self):
        """
        Test the S matrix against the example from the slides
        """
        expected = numpy.matrix([
            [0.0, 1.0 / 2.0, 1.0 / 2.0, 0.0, 0.0, 0.0],
            [1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0],
            [1.0 / 3.0, 1.0 / 3.0, 0.0, 0.0, 1.0 / 3.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0 / 2.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 2.0, 0.0, 1.0 / 2.0],
            [0.0, 0.0, 0.0, 1.0 / 1.0, 0.0, 0.0]
        ], numpy.float64)
        self.graph.create_h_matrix()
        self.graph.create_s_matrix()
        self.graph.describe_matrix(self.graph.s_matrix)
        numpy.testing.assert_allclose(self.graph.s_matrix, expected)

    def test_g_matrix(self):
        """
        Test the G matrix against the example from the slides
        """
        expected = numpy.matrix([
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
        self.graph.describe_matrix(self.graph.g_matrix)
        numpy.testing.assert_allclose(self.graph.g_matrix, expected)

    def test_pi_vector(self):
        """
        Test the Pi vector
        """
        expected = numpy.matrix([0.03721, 0.05396, 0.04151, 0.3751, 0.206, 0.2862], numpy.float64)
        expected.round(4, expected)
        self.graph.create_h_matrix()
        self.graph.create_s_matrix()
        self.graph.create_g_matrix(damping_factor=0.9)
        self.graph.create_pi_vector()
        self.graph.pi_vector.round(4, self.graph.pi_vector)
        self.graph.describe_matrix(self.graph.pi_vector)
        numpy.testing.assert_allclose(self.graph.pi_vector, expected)

    def test_ranks(self):
        """
        Test the final rankings
        """
        expected = ['P4', 'P6', 'P5', 'P2', 'P3', 'P1']
        self.graph.create_h_matrix()
        self.graph.create_s_matrix()
        self.graph.create_g_matrix(damping_factor=0.9)
        self.graph.create_pi_vector()
        self.graph.compute_page_rank()
        self.assertListEqual(self.graph.rankings, expected)
