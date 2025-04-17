# -Un-Installer

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-Apache--2.0-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![Version](https://img.shields.io/badge/Version-1.0.0-lightgrey)

[中文](README_CN.md)

A Tkinter-based GUI tool for Python package management with multi-source and batch operation support.

## Features

- 🚀 One-click install/upgrade/uninstall Python packages
- 🌍 Support multiple mirror sources (Aliyun, PyPI, Tsinghua University, etc.)
- 📦 Automatically redirect to PyPI package details page
- 📁 Batch operations from requirements.txt files
- ⚙️ Multi-threaded execution to prevent UI freezing
- 🌐 Bilingual interface (Chinese and English)
- 📜 Real-time command output display
- 🔒 Disable buttons during execution to prevent misoperation
- 🖥️ Console-style output display with monospace font
- ⚙️ Configurable language and default mirror source

## Requirements

- Python 3.6 +
- Tkinter (usually included in Python standard library)
- Required Python standard libraries:
  - `subprocess`
  - `threading`
  - `webbrowser`
  - `tkinter`
  - `tkinter.ttk`

## Usage

1. Enter package name in the text box (or select files for batch operations)
2. Select a mirror source (default: PyPI)
3. Click the corresponding function button:
   - **Install**: Install the latest version from the selected source
   - **Upgrade**: Upgrade to the latest version
   - **Uninstall**: Completely remove the package
   - **Details**: Open the PyPI page of the package
   - **Settings**: Change language and default mirror source
   - **About**: View version information and source code
4. View real-time execution results in the output box below

## Technical Details

- Uses `subprocess.Popen` to call system pip commands
- Implements asynchronous operations through `threading.Thread`
- Automatically captures and displays command output
- Uses monospace font `Consolas` for output display
- Error handling mechanism:
  - Catches all exceptions and displays error dialog
  - Shows standard error output
  - Disables all operation buttons during execution
- Uses `Toplevel` for about and settings windows
- Implements modern `ttk` themed widgets
- Persistent storage of configuration data

## Supported Sources

| Name                | URL                                      |
|---------------------|------------------------------------------|
| Aliyun             | https://mirrors.aliyun.com/pypi/simple   |
| PyPI               | https://pypi.org/simple                  |
| Tsinghua University| https://pypi.tuna.tsinghua.edu.cn/simple |

You can add custom sources by modifying `data.json`.

## UI Structure

```
[Package Name Entry] [Source Combobox]

[Install Button]     [Upgrade Button]
[Uninstall Button]   [Details Button]
[Settings Button]    [About Button]

[Batch Operations Panel]
[File List]         [Add Files Button]

[Output Text Area]
```

## Contributing

Welcome to submit `Issue` and `Pull Request`:

1. `Fork` the repository
2. Create a feature branch 
    ```bash
    git checkout -b feature/new-feature
    ```
3. Commit your changes
    ```bash
    git commit -am 'Add new feature'
    ```
4. Push the branch
    ```bash
    git push origin feature/new-feature
    ```
5. Create a new `Pull Request`
