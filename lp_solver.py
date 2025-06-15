from graph import Graph
from bipartite_vertex_cover_solver import BipartiteVertexCoverSolver

class LPSolver:
    def solve_half_integral(self, G: Graph):
        """
        Solves LP relaxation for Vertex Cover and returns:
        - True if not all values are 0.5
        - Dictionary {v: 0, 0.5, or 1} for each vertex
        """
        edges = [(u, v + G.n) for u, v in G.edges] + [(u + G.n, v) for u, v in G.edges]
        
        solver = BipartiteVertexCoverSolver(G.n, G.n * 2, edges)

        vc = solver.find_vertex_cover()

        lp_solution = self.get_lp_from_vc(vc, G.n)

        if not self.check_if_all_half(lp_solution, G):
             return False, lp_solution


        for v in range(G.n):
            for u in G.get_neighbors(v):
                solver.remove_edge(u, v + G.n)
                solver.remove_edge(u + G.n, v)
            
            vc_modified = solver.find_vertex_cover()

            if len(vc_modified) + 2 == len(vc):
                lp_solution_modified = self.get_lp_from_vc(vc_modified, G.n)
                lp_solution_modified[v] = 1
                return False, lp_solution_modified
            
            for u in G.get_neighbors(v):
                solver.add_edge(u, v + G.n)
                solver.add_edge(u + G.n, v)         

        return True, lp_solution
        
    def get_lp_from_vc(self, vc, n):
            result = {v : 0 for v in range(n)}
            
            for v in vc:
                result[v % n] += 0.5
            
            return result
    
    def check_if_all_half(self, solution, graph):
        for v, val in solution.items():
            if abs(val - 1.0) < 1e-6:
                return False
            if abs(val - 0.0) < 1e-6 and graph.get_neighbors(v):
                return False
        return True