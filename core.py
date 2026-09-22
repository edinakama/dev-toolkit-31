import time
from typing import Callable, Any, List

class AcceleratedRunner:
    """Dynamic function unroller and JIT-style chain compiler."""

    def __init__(self, *steps: Callable[[Any], Any]):
        self._steps: List[Callable[[Any], Any]] = list(steps)
        self._fast_fn: Callable[[Any], Any] = self._build_fast_path()

    def _build_fast_path(self) -> Callable[[Any], Any]:
        if not self._steps:
            return lambda x: x

        func_names = [f"_fn_{i}" for i in range(len(self._steps))]
        env = {func_names[i]: fn for i, fn in enumerate(self._steps)}

        lines = ["def __fast_run(data):"]
        lines.append("    res = data")
        for name in func_names:
            lines.append(f"    res = {name}(res)")
        lines.append("    return res")

        exec("\n".join(lines), env)
        return env["__fast_run"]

    def pipe(self, step: Callable[[Any], Any]) -> "AcceleratedRunner":
        self._steps.append(step)
        self._fast_fn = self._build_fast_path()
        return self

    def run(self, data: Any) -> Any:
        return self._fast_fn(data)

    def benchmark_and_warmup(self, sample_data: Any, iterations: int = 100) -> float:
        start = time.perf_counter()
        for _ in range(iterations):
            self._fast_fn(sample_data)
        return (time.perf_counter() - start) / iterations
