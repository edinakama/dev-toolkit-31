"""Dynamic task synthesis and execution engine for dev-toolkit-31."""

from typing import TypeVar, Callable, Generic, Any, List, Tuple
import inspect

T = TypeVar("T")
R = TypeVar("R")


class Node(Generic[T, R]):
    """A wrapper node representing a transformation step in an execution graph."""

    def __init__(self, action: Callable[[T], R], name: str | None = None) -> None:
        """Initialize a transformation node with a call target and optional alias."""
        self.action: Callable[[T], R] = action
        self.name: str = name or action.__name__

    def __call__(self, payload: T) -> R:
        """Execute the node action with type introspection enforcement."""
        sig = inspect.signature(self.action)
        bound = sig.bind(payload)
        bound.apply_defaults()
        return self.action(*bound.args, **bound.kwargs)

    def __rshift__(self, next_node: "Node[R, Any]") -> "Pipeline[T, Any]":
        """Overload >> operator to compose nodes into a processing pipeline."""
        return Pipeline(self) >> next_node


class Pipeline(Generic[T, R]):
    """Sequential execution pipeline composed using bitwise shift operators."""

    def __init__(self, initial: Node[T, Any]) -> None:
        """Construct pipeline starting with an initial node."""
        self._chain: List[Node[Any, Any]] = [initial]

    def __rshift__(self, next_node: Node[Any, Any]) -> "Pipeline[T, Any]":
        """Append another node onto the existing execution chain."""
        self._chain.append(next_node)
        return self

    def execute(self, initial_value: T) -> Any:
        """Run the initial value through all connected nodes in order."""
        accumulator: Any = initial_value
        for node in self._chain:
            accumulator = node(accumulator)
        return accumulator

    def inspect_chain(self) -> List[Tuple[str, str]]:
        """Return metadata about steps and their signature representations."""
        return [(n.name, str(inspect.signature(n.action))) for n in self._chain]


def step(alias: str | None = None) -> Callable[[Callable[[T], R]], Node[T, R]]:
    """Decorator converting raw functions into typed pipeline execution nodes."""
    def decorator(fn: Callable[[T], R]) -> Node[T, R]:
        return Node(fn, name=alias)
    return decorator
