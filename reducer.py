class Reducer:
    def apply(self, G, solution, k):
        """
        Applies standard LP-based reduction rules.
        Removes 0s and includes 1s into vertex cover.
        Returns: new_G, new_k, vertices_added_to_vc
        """
        vertices_to_remove = []
        added_to_vc = []

        for v, val in solution.items():
            if val == 1:
                vertices_to_remove.append(v)
                added_to_vc.append(v)
                k -= 1
            elif val == 0:
                vertices_to_remove.append(v)

        return G.copy_without_vertices(vertices_to_remove), k, added_to_vc
