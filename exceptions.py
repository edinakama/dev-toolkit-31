import inspect
from typing import Any, Dict, Type


class ToolkitError(Exception):
    """Base exception for dev-toolkit-31 with automatic call-stack context harvesting."""

    def __init__(self, message: str, **kwargs: Any):
        self.payload = kwargs
        # Dynamically inspect caller's frame to harvest diagnostic data automatically
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller = frame.f_back
            self.payload["caller_module"] = caller.f_globals.get("__name__", "unknown")
            self.payload["caller_line"] = caller.f_lineno
            self.payload["caller_locals"] = {
                k: repr(v)[:80] 
                for k, v in caller.f_locals.items() 
                if not k.startswith("__")
            }
        
        context_str = ", ".join(f"{k}={v}" for k, v in self.payload.items())
        full_msg = f"{message} | Context: {{{context_str}}}" if context_str else message
        super().__init__(full_msg)


class EdgeCaseErrorFactory:
    """A factory that dynamically synthesizes unique exception types on the fly to avoid boilerplate."""

    _registry: Dict[str, Type[ToolkitError]] = {}

    @classmethod
    def raise_dynamic(cls, name: str, reason: str, **metadata: Any) -> None:
        """Synthesizes and raises a highly customized exception type."""
        normalized_name = "".join(part.capitalize() for part in name.split())
        if not normalized_name.endswith("Error"):
            normalized_name += "Error"

        if normalized_name not in cls._registry:
            # Generate unique exception class dynamically at runtime
            new_exception_type = type(
                normalized_name,
                (ToolkitError,),
                {"__doc__": f"Dynamically generated error representing {reason}.", "category": name},
            )
            cls._registry[normalized_name] = new_exception_type

        raise cls._registry[normalized_name](f"Dynamic Failure: {reason}", **metadata)


# Pre-cooked creative exceptions for exotic edge-cases
HeisenbugError = EdgeCaseErrorFactory.raise_dynamic
