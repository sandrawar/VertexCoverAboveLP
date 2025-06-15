from graph_loader import GraphLoader
from vc_tester import VcTester

from os import path

if __name__ == "__main__":
    
    tester = VcTester()
    graph_loader = GraphLoader()
    
    print("Proste testy...")
    for i in range(7):
        filename = path.join("test_graphs", "basic", f"case_{i}.txt")

        graph, name, k = graph_loader.load_from_file(filename)

        print(f"Test {i} - {name}:")

        tester.test(graph, k)

    print("Większe testy...")
    for i in range(10):
        filename = path.join("test_graphs", "big", f"case_{i}.txt")

        graph, _, k = graph_loader.load_from_file(filename)

        print(f"Test {i} - graf o {graph.n} wierzchołkach i {len(graph.get_edges())} krawędziach:")

        tester.test(graph, k)
    
    

