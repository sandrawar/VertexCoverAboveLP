import time
from vc_solver import VcSolver
from graph import Graph

class VcTester:
    def __init__(self, solver=None):
        self.solver = solver if solver else VcSolver()

    def test(self, graph, k):
        print(f"Testing Vertex Cover with k = {k}...")
        start_time = time.perf_counter()
        result, cover = self.solver.solve(graph, k)
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        if result:
            print(f"✔️  Vertex Cover found: {sorted(cover)}")
            if self._validate_cover(graph, cover):
                print("✅  The solution is a valid vertex cover.")
            else:
                print("❌  The solution is NOT a valid vertex cover.")
        else:
            print("❌  No vertex cover of size ≤ k found.")

        print(f"⏱️  Time taken: {elapsed:.6f} seconds\n")

    def _validate_cover(self, graph, cover):
        """
        Check whether the given set of vertices covers all edges.
        """
        cover_set = set(cover)
        for u, v in graph.get_edges():
            if u not in cover_set and v not in cover_set:
                return False
        return True
