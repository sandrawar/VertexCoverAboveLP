import unittest
from graph import Graph
from vc_solver import VcSolver

class TestVertexCover(unittest.TestCase):

    def setUp(self):
        # Simple graph (triangle)
        self.G1 = Graph(3)  # A triangle with 3 vertices
        self.G1.add_edge(0, 1)
        self.G1.add_edge(1, 2)
        self.G1.add_edge(0, 2)

        # Linear graph (path)
        self.G2 = Graph(4)  # A path with 4 vertices
        self.G2.add_edge(0, 1)
        self.G2.add_edge(1, 2)
        self.G2.add_edge(2, 3)

        # Empty graph
        self.G3 = Graph(5)  # A graph with 5 vertices and no edges

        # Star graph (vertex 0 connected to vertices 1..4)
        self.G4 = Graph(5)  # A star-shaped graph with 5 vertices
        for i in range(1, 5):
            self.G4.add_edge(0, i)

        self.solver = VcSolver()

    def test_triangle_graph(self):
        result, cover = self.solver.solve(self.G1, k=2)
        self.assertTrue(result)  
        self.assertLessEqual(len(cover), 2)  

    def test_path_graph(self):
        result, cover = self.solver.solve(self.G2, k=2)
        self.assertTrue(result)  
        self.assertLessEqual(len(cover), 2)

    def test_empty_graph(self):
        result, cover = self.solver.solve(self.G3, k=0)
        self.assertTrue(result)  
        self.assertEqual(len(cover), 0)  

    #def test_star_graph(self):
    #    result, cover = self.solver.solve(self.G4, k=1)
    #    self.assertTrue(result)  
    #    self.assertLessEqual(len(cover), 1)  

    def test_too_small_k(self):
        result, cover = self.solver.solve(self.G2, k=1)
        self.assertFalse(result)  
        self.assertIsNone(cover)  

if __name__ == '__main__':
    unittest.main()
