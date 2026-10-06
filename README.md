# dev-toolkit-31

`dev-toolkit-31` is a robust Python utility suite designed to streamline routine development tasks and automate common command-line operations. It provides a centralized hub for environment management, file processing, and local server orchestration to boost developer productivity.

### Key Features

*   **Project Scaffolding:** Rapidly generate standardized directory structures and boilerplate configurations for new Python projects.
*   **Environment Sync:** Effortlessly synchronize environment variables and dependency files across local and staging configurations.
*   **Log Analytics:** An embedded lightweight parser to filter, search, and aggregate data from application logs in real-time.
*   **Task Runner:** A streamlined wrapper to manage concurrent execution of linters, formatters, and test suites with custom task definitions.

### Installation

Requires Python 3.9 or higher. Install the toolkit globally or within your virtual environment:

```bash
# Clone the repository
git clone https://github.com/Developer/dev-toolkit-31.git
cd dev-toolkit-31

# Install requirements
pip install -r requirements.txt

# Install as a package
pip install .
```

### Usage

Once installed, you can trigger specific toolkit modules via the `dtk` command.

**Running a project build:**
```bash
dtk scaffold --name my-new-app --template fastapi
```

**Parsing logs from a file:**
```bash
dtk logs parse ./app.log --level ERROR --output report.json
```

For a full list of commands and available flags, run:
```bash
dtk --help
```

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.