from graph import Graph
from helpers import *


def branching(G, k, lp_val):
    """
    Recursive branching algorithm for solving the Vertex Cover problem using LP relaxation
    and a half-integral solution approach.

    Parameters:
    - G: Graph object (custom Graph class)
    - k: Integer, the size limit of the vertex cover
    - lp_val: Float, the LP-relaxation value of the current graph

    Returns:
    - True if a vertex cover of size ≤ k exists
    - False otherwise
    """

    if lp_val > k:
        return False

    solution = solve_lpvc_half_integral(G)

    if not is_all_half(solution):
        G_reduced, k_reduced = apply_reduction(G, solution, k)
        return branching(G_reduced, k_reduced, lp_val)

    if number_of_vertices_remaining(G) == 0:
        return True

    for v in G.get_vertices():
        if G.get_neighbors(v):
            break

    neighbors = G.get_neighbors(v)

    G1 = G.copy_without_vertices([v])
    if branching(G1, k - 1, solve_lpvc_half_integral(G1)):
        return True

    G2 = G.copy_without_vertices(neighbors + [v])
    if branching(G2, k - len(neighbors), solve_lpvc_half_integral(G2)):
        return True

    return False
