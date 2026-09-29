import inspect
from typing import Callable, Any, Dict, List, Type, get_type_hints

class DynamicHandler:
    """
    A handler that dynamically routes event payloads to registered callbacks
    based on the parameter type annotations of those callbacks.
    """

    def __init__(self) -> None:
        self._registry: Dict[Type[Any], List[Callable[[Any], Any]]] = {}

    def register(self, callback: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """
        Registers a callback by inspecting its first parameter's type annotation.

        Args:
            callback: A callable taking at least one annotated parameter.

        Returns:
            The registered callback unmodified.
        """
        sig = inspect.signature(callback)
        params = list(sig.parameters.values())
        if not params:
            raise ValueError("Callback must accept at least one argument.")

        hints = get_type_hints(callback)
        param_name = params[0].name
        param_type = hints.get(param_name, Any)

        if param_type not in self._registry:
            self._registry[param_type] = []
        self._registry[param_type].append(callback)
        return callback

    def emit(self, payload: Any) -> List[Any]:
        """
        Dispatches the payload to all callbacks registered for its exact type
        or a superclass of its type.

        Args:
            payload: The input data event to process.

        Returns:
            A list of returned results from matching callbacks.
        """
        results: List[Any] = []
        payload_type = type(payload)

        for registered_type, callbacks in self._registry.items():
            try:
                matches = issubclass(payload_type, registered_type)
            except TypeError:
                matches = registered_type is Any

            if matches:
                for callback in callbacks:
                    results.append(callback(payload))
        return results
