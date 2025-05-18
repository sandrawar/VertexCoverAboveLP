class Graph:
    def __init__(self, n):
        """
        Initialize a graph with n vertices.
        Vertices are numbered from 0 to n - 1.
        """
        self.n = n
        self.edges = set()
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v):
        """
        Add an undirected edge between vertices u and v.
        """
        if u == v:
            return  
        if (u, v) not in self.edges and (v, u) not in self.edges:
            self.edges.add((u, v))
            self.adj[u].append(v)
            self.adj[v].append(u)

    def remove_edge(self, u, v):
        """
        Remove an undirected edge between u and v.
        """
        if (u, v) in self.edges:
            self.edges.remove((u, v))
        elif (v, u) in self.edges:
            self.edges.remove((v, u))
        else:
            return 
        self.adj[u].remove(v)
        self.adj[v].remove(u)

    def remove_vertex(self, v):
        """
        Remove vertex v and all incident edges.
        """
        for neighbor in list(self.adj[v]):
            self.remove_edge(v, neighbor)
        self.adj[v] = []

    def get_neighbors(self, v):
        """
        Return a list of neighbors of vertex v.
        """
        return self.adj[v]

    def get_edges(self):
        """
        Return a list of all undirected edges.
        """
        return list(self.edges)

    def get_vertices(self):
        """
        Return a list of all vertex indices.
        """
        return list(range(self.n))

    def induced_subgraph(self, vertex_set):
        """
        Create an induced subgraph over a subset of vertices.
        """
        index_map = {v: i for i, v in enumerate(vertex_set)}
        subgraph = Graph(len(vertex_set))
        for u in vertex_set:
            for v in self.adj[u]:
                if v in index_map and index_map[u] < index_map[v]: 
                    subgraph.add_edge(index_map[u], index_map[v])
        return subgraph
