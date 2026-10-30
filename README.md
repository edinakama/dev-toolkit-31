# dev-toolkit-31

A collection of high-performance Python utilities designed to streamline daily development workflows and automate repetitive CLI tasks. This toolkit provides a robust foundation for project scaffolding, environment management, and text processing.

## Features

*   **Project Scaffolder:** Rapidly generate standardized directory structures and boilerplate configurations for Python-based applications.
*   **Environment Validator:** Automated diagnostic tool to check for missing dependencies, incorrect Python versions, and broken environment variables.
*   **File Stream Processor:** High-efficiency utility for mass refactoring, pattern matching, and file renaming across nested directories.
*   **Log Formatter:** Custom parser that turns cluttered raw application logs into structured, human-readable tables.

## Installation

Ensure you have Python 3.9+ installed. You can install the toolkit directly via pip:

```bash
# Clone the repository
git clone https://github.com/Developer/dev-toolkit-31.git
cd dev-toolkit-31

# Install requirements
pip install -r requirements.txt

# Install as an editable package
pip install -e .
```

## Basic Usage

Once installed, you can access the toolkit functionality through the `dtk` command line interface. 

To run a project health check in your current directory:

```bash
dtk validate --env production
```

To scaffold a new microservice structure in a target folder:

```bash
dtk scaffold --type service --name auth-gateway
```

You can view the full list of available commands and their arguments by running:

```bash
dtk --help
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.