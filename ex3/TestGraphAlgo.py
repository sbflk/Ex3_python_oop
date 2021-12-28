import unittest
from threading import Thread

from GraphAlgo import GraphAlgo
from DiGraph import DiGraph
import time

class TestGraphAlgo(unittest.TestCase):



    def test_tsp(self):
        g = GraphAlgo()
        g1 = g.get_graph()
        x = 35.19805902663438
        y = 32.10525428067227
        for n in range(4):
            g1.add_node(n, (x, y))
        g1.add_edge(0, 1, 1)
        g1.add_edge(1, 0, 1.1)
        g1.add_edge(1, 2, 1.3)
        g1.add_edge(2, 3, 1.1)
        g1.add_edge(1, 3, 1.9)
        z = g.TSP([0, 1, 2])
        time.sleep(0.5)
        self.assertEqual(z[0], [0, 1, 2])
        time.sleep(0.5)
        self.assertEqual(z[1], 2.3)

    def test_center_point(self):
        g = GraphAlgo()
        g1 = g.get_graph()
        x = 35.19805902663438
        y = 32.10525428067227
        for n in range(4):
            g1.add_node(n, (x, y))
        g1.add_edge(0, 1, 1)
        g1.add_edge(1, 0, 1.1)
        g1.add_edge(1, 2, 1.3)
        g1.add_edge(2, 3, 1.1)
        g1.add_edge(1, 3, 1.9)
        z = g.centerPoint()
        self.assertEqual(z[0],1)
        self.assertEqual(z[1], 1.9)

    def test_shortest_path(self):
        g = GraphAlgo()
        g1 = g.get_graph()
        x = 35.19805902663438
        y = 32.10525428067227
        for n in range(4):
            g1.add_node(n, (x, y))
        g1.add_edge(0, 1, 1)
        g1.add_edge(1, 0, 1.1)
        g1.add_edge(1, 2, 1.3)
        g1.add_edge(2, 3, 1.1)
        g1.add_edge(1, 3, 1.9)
        z = g.shortest_path(1,2)
        self.assertEqual(z[0],1.3)
        self.assertEqual(z[1], [1,2])


if __name__ == '__main__':
    unittest.main()