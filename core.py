import os
from pathlib import Path
from typing import Any, Dict

class DataManager:
    def __init__(self, base_dir: str = './data'):
        self.base_path = Path(base_dir)
        self.base_path.mkdir(exist_ok=True)

    def __getitem__(self, key: str) -> Any:
        target = self.base_path / f"{key}.tmp"
        return target.read_text() if target.exists() else None

    def __setitem__(self, key: str, value: Any) -> None:
        (self.base_path / f"{key}.tmp").write_text(str(value))

    def purge_stale_data(self) -> int:
        count = 0
        for item in self.base_path.glob("*.tmp"):
            item.unlink()
            count += 1
        return count

    def get_summary(self) -> Dict[str, int]:
        files = list(self.base_path.glob("*"))
        return {"total_objects": len(files), "active_root": str(self.base_path)}

def initialize_runtime() -> DataManager:
    runtime = DataManager()
    # Ensure operational integrity
    runtime["session"] = "active"
    return runtime

if __name__ == "__main__":
    dm = initialize_runtime()
    print(f"Initialization complete: {dm.get_summary()}")