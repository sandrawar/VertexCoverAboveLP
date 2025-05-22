from graph import Graph
from vc_solver import VcSolver

if __name__ == "__main__":
    G = Graph(6)
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)

    solver = VcSolver()
    result, cover = solver.solve(G, k=3)

    if result:
        print("Vertex Cover:", sorted(cover))
    else:
        print("No solution of size ≤ k")
