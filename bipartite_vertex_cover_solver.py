class MatchingEdge:
    """
    Represents an undirected edge in the graph, with an indicator whether it belongs to the matching.
    """
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.is_in_matching = False

    def get_other_vertex(self, w):
        """
        Given one vertex of the edge, returns the opposite vertex.
        """
        return self.v if w == self.u else self.u
    
    def __str__(self):
        return f"({self.u}, {self.v}){'*' if self.is_in_matching else ''}"
    def __repr__(self):
        return self.__str__()


class BipartiteVertexCoverSolver:
    """
    Solver for finding maximum matching and minimum vertex cover in a bipartite graph.
    """
    def __init__(self, left_partition_size, num_vertices, edges):
        self.left_partition_size = left_partition_size
        self.num_vertices = num_vertices
        self.edges = []

        # Adjacency structures
        self.edges_adj_list = [[] for _ in range(num_vertices)]
        self.edge_adj_matrix = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]

        for u, v in edges:
            edge = MatchingEdge(u, v)
            self.edge_adj_matrix[u][v] = edge
            self.edge_adj_matrix[v][u] = edge
            self.edges_adj_list[u].append(edge)
            self.edges_adj_list[v].append(edge)
            self.edges.append(edge)
        
        self.is_vertex_free = [True for _ in range(self.num_vertices)]

    def add_edge(self, u, v):
        """
        Adds an undirected edge between u and v to the graph.
        """
        if self.edge_adj_matrix[u][v] is not None:
            return

        edge = MatchingEdge(u, v)
        self.edge_adj_matrix[u][v] = edge
        self.edge_adj_matrix[v][u] = edge
        self.edges_adj_list[u].append(edge)
        self.edges_adj_list[v].append(edge)
        self.edges.append(edge)

    def remove_edge(self, u, v):
        """
        Removes the undirected edge between u and v from the graph.
        """
        edge = self.edge_adj_matrix[u][v]
        if edge is None:
            return
        
        if edge.is_in_matching:
            self.is_vertex_free[v] = True
            self.is_vertex_free[u] = True

        if edge in self.edges_adj_list[u]:
            self.edges_adj_list[u].remove(edge)
        if edge in self.edges_adj_list[v]:
            self.edges_adj_list[v].remove(edge)
        if edge in self.edges:
            self.edges.remove(edge)

        self.edge_adj_matrix[u][v] = None
        self.edge_adj_matrix[v][u] = None

    def find_matching(self):
        """
        Finds a maximum matching using layered BFS and DFS.
        """
        while True:
            num_layers, layers = self.find_layers()
            if num_layers == 0:
                break

            paths = self.find_paths_from_layers(layers)

            for path in paths:
                self.change_matching_along_alternating_path(path)

    def find_layers(self):
        """
        Builds layers (BFS style) from free vertices on the left side.
        Returns the number of layers and the layer assignment per vertex.
        """
        layers = [-1 for _ in range(self.num_vertices)]
        current_layer = [v for v in range(self.left_partition_size) if self.is_vertex_free[v]]
        next_layer = []
        num_layers = 1
        should_edge_be_matching = False
        found_free_vertex_on_right = False

        while True:
            if not current_layer:
                if found_free_vertex_on_right:
                    return (num_layers, layers)
                if not next_layer:
                    break
                current_layer, next_layer = next_layer, []
                num_layers += 1
                should_edge_be_matching = not should_edge_be_matching

            v = current_layer.pop()
            if layers[v] != -1:
                continue

            layers[v] = num_layers - 1

            if num_layers != 1 and self.is_vertex_free[v]:
                found_free_vertex_on_right = True

            for e in self.get_neighbours(v, should_edge_be_matching):
                u = e.get_other_vertex(v)
                if layers[u] == -1:
                    next_layer.append(u)

        return (0, [])
    
    def find_paths_from_layers(self, layers):
        """
        For each free vertex in layer 0, perform DFS to find alternating paths.
        """
        paths = []
        for v in self.get_layer_vertices(layers, 0):
            path = self.layers_dfs(v, layers)
            if path:
                paths.append(path)
        return paths

    def layers_dfs(self, v, layers):
        """
        DFS to find an alternating path from a layered graph.
        """
        if layers[v] == -1:
            return []

        for e in self.get_neighbours_from_next_layer(v, layers):
            if e.is_in_matching == (layers[v] % 2 == 0):
                continue

            u = e.get_other_vertex(v)
            u_path = self.layers_dfs(u, layers)
            if len(u_path) > 0:
                layers[v] = -1
                return [v] + u_path

        if self.is_vertex_free[v] and layers[v] != 0:
            layers[v] = -1
            return [v]

        layers[v] = -1
        return []

    def find_vertex_cover(self):
        """
        Uses the König's algorithm logic to extract the minimum vertex cover
        from the maximum matching.
        """
        self.find_matching()
        visited = [False for _ in range(self.num_vertices)]

        # Start DFS from free vertices on the left partition
        start_vertices = [v for v in range(self.left_partition_size)
                          if self.get_partition(v) == 0 and self.is_vertex_free[v]]
        

        for v in start_vertices:
            self.vertex_cover_dfs(v, visited)

        vertex_cover = []
        for v in range(self.left_partition_size):
            if not visited[v]:
                vertex_cover.append(v)
        for v in range(self.left_partition_size, self.num_vertices):
            if visited[v]:
                vertex_cover.append(v)

        return vertex_cover

    def vertex_cover_dfs(self, v, visited):
        """
        DFS used for vertex cover extraction.
        """
        if visited[v]:
            return
        visited[v] = True

        should_edge_be_in_matching = self.get_partition(v) == 1

        for e in self.get_neighbours(v, should_edge_be_in_matching):
            u = e.get_other_vertex(v)
            self.vertex_cover_dfs(u, visited)

    def get_neighbours(self, v, should_edge_be_in_matching):
        """
        Returns neighbours of vertex v via edges that are (or aren't) in the matching.
        """
        return [e for e in self.edges_adj_list[v] if e.is_in_matching == should_edge_be_in_matching]

    def get_partition(self, v):
        """
        Returns 0 if vertex is in left partition, 1 otherwise.
        """
        return 0 if v < self.left_partition_size else 1

    def get_neighbours_from_next_layer(self, v, layers):
        """
        Returns neighbours of v that are in the next layer.
        """
        return [e for e in self.edges_adj_list[v]
                if layers[v] != -1 and layers[v] + 1 == layers[e.get_other_vertex(v)]]

    def get_layer_vertices(self, layers, layer_index):
        """
        Returns list of vertices in a given layer.
        """
        return [v for v in range(self.num_vertices) if layers[v] == layer_index]

    def change_matching_along_alternating_path(self, path):
        """
        Flips the matching status of edges along an alternating path.
        """
        if not path:
            return

        for u, v in zip(path, path[1:]):
            self.edge_adj_matrix[u][v].is_in_matching = not self.edge_adj_matrix[u][v].is_in_matching

        self.is_vertex_free[path[0]] = False
        self.is_vertex_free[path[-1]] = False
