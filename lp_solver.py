class LPSolver:
    def solve_half_integral(self, G):
        """
        Solves LP relaxation for Vertex Cover and returns:
        - True if feasible
        - Dictionary {v: 0, 0.5, or 1} for each vertex
        """
        # Placeholder/mock
        solution = {v: 0.5 for v in range(G.n) if G.get_neighbors(v)}
        return True, solution
