from lp_solver import LPSolver
from reducer import Reducer

class VcSolver:
    def __init__(self):
        self.lp_solver = LPSolver()
        self.reducer = Reducer()

    def solve(self, G, k):
        lp_ok, solution = self.lp_solver.solve_half_integral(G)
        if not lp_ok:
            return False, None

        lp_val = sum(solution.values())
        return self._branch(G, k, lp_val, set())

    def _branch(self, G, k, lp_val, chosen):
        """
        Recursive branching algorithm for solving the Vertex Cover problem using LP relaxation
        and a half-integral solution approach.

        Parameters:
        - G: Graph object
        - k: Integer, size limit of the vertex cover
        - lp_val: Float, LP-relaxation value
        - chosen: Set, current solution

        Returns:
        - (True, set) if a vertex cover of size ≤ k exists
        - (False, None) otherwise
        """

        if lp_val > k:
            return False, None

        lp_ok, solution = self.lp_solver.solve_half_integral(G)
        if not lp_ok:
            return False, None

        if not self._is_all_half(solution):
            G_red, k_red, added = self.reducer.apply(G, solution, k)
            chosen |= set(added)
            _, new_solution = self.lp_solver.solve_half_integral(G_red)
            new_lp = sum(new_solution.values())
            return self._branch(G_red, k_red, new_lp, chosen)

        if not G.get_edges():
            return True, chosen

        for v in G.get_vertices():
            if G.get_neighbors(v):
                break

        neighbors = G.get_neighbors(v)

        # Branch: pick v
        G1 = G.copy_without_vertices([v])
        _, sol1 = self.lp_solver.solve_half_integral(G1)
        lp1 = sum(sol1.values())
        res1, cover1 = self._branch(G1, k - 1, lp1, chosen | {v})
        if res1:
            return True, cover1

        # Branch: pick all neighbors
        G2 = G.copy_without_vertices(neighbors)
        _, sol2 = self.lp_solver.solve_half_integral(G2)
        lp2 = sum(sol2.values())
        res2, cover2 = self._branch(G2, k - len(neighbors), lp2, chosen | set(neighbors))
        if res2:
            return True, cover2

        return False, None

    def is_all_half(solution):
        return all(abs(val - 0.5) < 1e-6 for val in solution.values())



