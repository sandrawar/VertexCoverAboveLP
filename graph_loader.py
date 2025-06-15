from graph import Graph

class GraphLoader:
    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        
        name = lines[0]              # nazwa grafu
        k = int(lines[1])            # maksymalny rozmiar vertex cover
        num_vertices = int(lines[2])  # liczba wierzchołków
        
        graph = Graph(num_vertices)
        
        for line in lines[3:]:
            u, v = map(int, line.split())
            graph.add_edge(u, v)

        return graph, name, k