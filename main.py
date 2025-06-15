from graph_loader import GraphLoader
from vc_tester import VcTester

from os import path

if __name__ == "__main__":
    
    tester = VcTester()
    graph_loader = GraphLoader()
    
    print("Proste testy...")
    for i in range(6):
        filename = path.join("test_cases", "basic", f"case_{i}.txt")

        graph, name, k = graph_loader.load_from_file(filename)

        print(f"Test {i} - {name}:")

        tester.test(graph, k)

