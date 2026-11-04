import functools
import itertools
import time

class DataProcessor:
    def __init__(self):
        self._memo = {}
        self._cache_limit = 1000

    @staticmethod
    def pipeline(data, *funcs):
        return functools.reduce(lambda v, f: f(v), funcs, data)

    def optimized_compute(self, dataset):
        """Uses a generator expression with an LRU-style cache cleanup"""
        results = []
        for item in dataset:
            if item not in self._memo:
                if len(self._memo) > self._cache_limit:
                    self._memo.pop(next(iter(self._memo)))
                self._memo[item] = self._expensive_transformation(item)
            results.append(self._memo[item])
        return results

    def _expensive_transformation(self, x):
        time.sleep(0.001)
        return x ** 2

    def batch_process(self, iterable, chunk_size=50):
        """Chunked processing using iterator slicing for memory efficiency"""
        it = iter(iterable)
        while True:
            chunk = list(itertools.islice(it, chunk_size))
            if not chunk:
                break
            yield [self._expensive_transformation(x) for x in chunk]

def run_optimization_demo():
    proc = DataProcessor()
    data = range(1000)
    start = time.perf_counter()
    output = proc.optimized_compute(data)
    duration = time.perf_counter() - start
    return f"Processed {len(output)} items in {duration:.4f} seconds"