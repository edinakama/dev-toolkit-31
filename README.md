# dev-toolkit-31

A high-performance Python utility suite designed to streamline local development workflows and automate repetitive CLI tasks. It provides a robust framework for project scaffolding, environment management, and code linting across multiple repositories.

## Features

*   **Scaffold Automation:** Quickly initialize project structures with pre-configured boilerplate templates for Flask, FastAPI, and custom CLI tools.
*   **Environment Sync:** Synchronize local virtual environment dependencies and environment variables across cross-platform setups seamlessly.
*   **Lint & Format Engine:** Integrated wrapper for Black, Flake8, and Mypy that enforces project-wide code standards with a single command.
*   **Log Analytics:** Lightweight log parsing utility that extracts and summarizes error patterns from local application logs for faster debugging.

## Installation

Ensure you have Python 3.9+ installed. Install the toolkit directly from the repository using pip:

```bash
git clone https://github.com/Developer/dev-toolkit-31.git
cd dev-toolkit-31
pip install -e .
```

## Usage

Once installed, use the `devtool` command to manage your projects. 

**Initialize a new project scaffold:**
```bash
devtool init --type fastapi --name my-web-app
```

**Run automated linting on your current directory:**
```bash
devtool lint --path ./src --fix
```

**Check the help menu for available modules:**
```bash
devtool --help
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.