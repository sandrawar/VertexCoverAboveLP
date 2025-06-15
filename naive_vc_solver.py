class NaiveVcSolver:
    def solve(self, G, k):
        return self._branch(G, k, set())

    def _branch(self, G, k, chosen):
        if k < 0:
            return False, None

        if not G.get_edges():
            return True, chosen

        # Wybierz dowolną krawędź
        for u, v in G.get_edges():
            break  # tylko pierwsza krawędź

        # Przypadek 1: dodaj u do pokrycia
        G1 = G.copy_without_vertices([u])
        res1, cover1 = self._branch(G1, k - 1, chosen | {u})
        if res1:
            return True, cover1

        # Przypadek 2: dodaj v do pokrycia
        G2 = G.copy_without_vertices([v])
        res2, cover2 = self._branch(G2, k - 1, chosen | {v})
        if res2:
            return True, cover2

        return False, None
