# dev-toolkit-31

A high-performance Python utility suite designed to streamline common developer workflows and system automation tasks. This toolkit minimizes boilerplate code, allowing you to focus on shipping robust software faster.

## Features

*   **Config Manager:** Rapidly initialize, validate, and parse YAML/JSON configuration files with type hinting.
*   **LogStreamer:** A thread-safe logging interface that formats structured output for terminal and file-based debugging simultaneously.
*   **EnvSync:** An automated environment validator that verifies system dependencies and secret availability before application startup.
*   **TaskBatcher:** A lightweight decorator-based wrapper for executing asynchronous batch processes with configurable retry logic.

## Installation

Ensure you have Python 3.9+ installed. You can install the toolkit directly via pip:

```bash
pip install dev-toolkit-31
```

For development installations, clone the repository and use poetry:

```bash
git clone https://github.com/Developer/dev-toolkit-31.git
cd dev-toolkit-31
poetry install
```

## Usage

Integrating `dev-toolkit-31` into your project is seamless. Here is an example of initializing the `ConfigManager` to load project settings:

```python
from dev_toolkit.config import ConfigManager

# Load and validate settings
config = ConfigManager(file_path="settings.yaml")

if config.is_valid():
    db_uri = config.get("database_uri")
    print(f"Connected to: {db_uri}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.