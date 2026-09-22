"""Dynamic context handler pipeline with conditional interception."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, Optional

Context = Dict[str, Any]
PipelineStep = Callable[[Context], Context]


@dataclass
class ExecutionResult:
    """Encapsulates the outcome of a pipeline processing pass."""

    payload: Context
    steps_executed: int = 0
    interrupted: bool = False


class ActionHandler:
    """Flexible event and task dispatch handler using layered generator pipelines."""

    def __init__(self, name: str = "default") -> None:
        """Initialize the action handler with an empty pipeline registry."""
        self.name: str = name
        self._chain: List[PipelineStep] = []

    def register(self, priority: int = 10) -> Callable[[PipelineStep], PipelineStep]:
        """Decorator to attach processing stages to the pipeline execution chain."""

        def decorator(func: PipelineStep) -> PipelineStep:
            setattr(func, "__priority__", priority)
            self._chain.append(func)
            self._chain.sort(key=lambda f: getattr(f, "__priority__", 10))
            return func

        return decorator

    def __call__(
        self,
        initial_state: Context,
        stop_condition: Optional[Callable[[Context], bool]] = None,
    ) -> ExecutionResult:
        """Execute registered handlers sequentially against mutating context state."""
        state: Context = initial_state.copy()
        executed_count: int = 0

        for step in self._chain:
            if stop_condition and stop_condition(state):
                return ExecutionResult(
                    payload=state,
                    steps_executed=executed_count,
                    interrupted=True,
                )
            state = step(state)
            executed_count += 1

        return ExecutionResult(
            payload=state,
            steps_executed=executed_count,
            interrupted=False,
        )

    def stream(
        self, states: Generator[Context, None, None]
    ) -> Generator[ExecutionResult, None, None]:
        """Yield execution results for a continuous stream of input contexts."""
        for ctx in states:
            yield self(ctx)
