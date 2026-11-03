import os
from typing import Dict, Any, List

class DataOrchestrator:
    def __init__(self, workspace: str):
        self.root = os.path.abspath(workspace)
        self.registry: Dict[str, List[Any]] = {}

    def ingest(self, key: str, payload: Any) -> None:
        if key not in self.registry:
            self.registry[key] = []
        self.registry[key].append(payload)

    def purge(self) -> None:
        self.registry.clear()

    @property
    def manifest(self) -> List[str]:
        return sorted(self.registry.keys())

    def serialize(self) -> Dict[str, Any]:
        return {k: [str(v) for v in vs] for k, vs in self.registry.items()}

    def __repr__(self) -> str:
        return f"<Orchestrator root={self.root} keys={len(self.manifest)}>"

def initialize_environment(path: str = ".") -> DataOrchestrator:
    instance = DataOrchestrator(path)
    if not os.path.exists(instance.root):
        os.makedirs(instance.root, exist_ok=True)
    return instance

if __name__ == "__main__":
    orchestrator = initialize_environment()
    orchestrator.ingest("config", {"mode": "debug"})
    print(orchestrator)