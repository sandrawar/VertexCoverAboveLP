import time
from vc_solver import VcSolver
from graph import Graph
from naive_vc_solver import NaiveVcSolver
from multiprocessing import Process, Queue


class VcTester:
    def __init__(self, solver=None, fallback_solver=None, timeout=100):
        self.solver = solver if solver else VcSolver()
        self.fallback_solver = fallback_solver if fallback_solver else NaiveVcSolver()
        self.timeout = timeout  # timeout in seconds

    def test(self, graph, k):
        print(f"🧪 Testowanie problemu Vertex Cover dla k = {k}...")
        start_time = time.perf_counter()
        result, cover = self.solver.solve(graph, k)
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        if result:
            print(f"✔️  Znaleziono pokrycie wierzchołkowe: {sorted(cover)}")
            if self._validate_cover(graph, cover):
                print("✅  Pokrycie jest poprawne – każda krawędź jest pokryta.")
            else:
                print("❌  Błąd – rozwiązanie nie pokrywa wszystkich krawędzi!")

            print("\n🔁 Uruchamianie naiwnego rozwiązania dla porównania (z limitem czasu)...")
            naive_result, naive_cover, naive_time, timed_out = self._run_naive_solver_with_timeout(graph, k)

            if timed_out:
                print(f"⚠️  Naiwny solver PRZEKROCZYŁ limit {self.timeout} sekund.")
            elif naive_result:
                print(f"🆗 Naiwny solver również znalazł pokrycie: {sorted(naive_cover)}")
                print(f"🐢 Czas działania naiwnego algorytmu: {naive_time:.6f} sekundy")
            else:
                print("⚠️  Naiwny solver NIE znalazł pokrycia.")
                print(f"🐢 Czas działania naiwnego algorytmu: {naive_time:.6f} sekundy")

        else:
            print("❌ Główny algorytm NIE znalazł pokrycia o rozmiarze ≤ k.")
            print("🔍 Sprawdzanie za pomocą naiwnego algorytmu (z limitem czasu)...")
            naive_result, naive_cover, naive_time, timed_out = self._run_naive_solver_with_timeout(graph, k)

            if timed_out:
                print(f"⚠️  Naiwny solver PRZEKROCZYŁ limit {self.timeout} sekund.")
            elif naive_result:
                print(f"❗ Naiwny solver ZNALAZŁ rozwiązanie: {sorted(naive_cover)}")
                print(f"🐢 Czas działania naiwnego algorytmu: {naive_time:.6f} sekundy")
            else:
                print("✅ Naiwny solver potwierdził brak pokrycia.")
                print(f"🐢 Czas działania naiwnego algorytmu: {naive_time:.6f} sekundy")

        print(f"⏱️  Czas działania głównego algorytmu: {elapsed:.6f} sekundy\n")

    def _validate_cover(self, graph, cover):
        cover_set = set(cover)
        for u, v in graph.get_edges():
            if u not in cover_set and v not in cover_set:
                return False
        return True

    def _run_naive_solver_with_timeout(self, graph, k):
        """
        Runs the naive solver in a separate process with a timeout.
        Returns (result, cover, time_taken, timed_out).
        """
        def target(q):
            start = time.perf_counter()
            result, cover = self.fallback_solver.solve(graph, k)
            end = time.perf_counter()
            q.put((result, cover, end - start))

        q = Queue()
        p = Process(target=target, args=(q,))
        p.start()
        p.join(self.timeout)

        if p.is_alive():
            p.terminate()
            p.join()
            return False, None, None, True  # Timed out

        result, cover, duration = q.get()
        return result, cover, duration, False
