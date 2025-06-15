import random
import os

def generate_random_graph(name, num_vertices, num_edges, k, directory="test_graphs/big"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v:
            edges.add((min(u, v), max(u, v)))  # unikamy duplikatów i pętli

    filename = os.path.join(directory, f"{name}.txt")
    with open(filename, "w") as f:
        f.write(f"{name}\n")
        f.write(f"{k}\n")
        f.write(f"{num_vertices}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

    print(f"Graph '{name}' with {num_vertices} vertices and {num_edges} edges saved to {filename}")

# 🔧 Przykład użycia:
if __name__ == "__main__":
    random.seed(42)  # dla powtarzalności

    # Parametry testów:
    for i in range(10):  # wygeneruj 5 grafów
        name = f"case_{i}"
        n = random.randint(50, 150)             # liczba wierzchołków
        m = random.randint(n, n * 4)            # liczba krawędzi (rzadki do gęstego grafu)
        k = random.randint(n //2, 2 * n // 3)           # przykładowe k
        generate_random_graph(name, n, m, k)


