# -Un-Installer

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-Apache--2.0-green)

一个基于 `Tkinter` 的 **Python包管理图形界面工具**，提供便捷的 `安装` / `升级` / `卸载` 操作，支持多镜像源选择。

A Tkinter-based GUI tool for Python package management with multi-source support.

## 功能特性 Features

- 🚀 一键安装/升级/卸载Python包  
  One-click install/upgrade/uninstall Python packages
- 🌍 支持多个镜像源（阿里云/PyPI/清华大学等）  
  Support multiple mirror sources (Aliyun, PyPI, Tsinghua University, etc.)
- 📦 自动跳转PyPI包详情页面  
  Automatically redirect to PyPI package details page
- ⚙️ 多线程执行防止界面冻结  
  Multi-threaded execution to prevent UI freezing
- 🎯 中英双语界面  
  Bilingual interface (Chinese and English)

## 安装要求 Requirements

- Python 3.6+
- Tkinter（通常包含在Python标准库中）  
  Tkinter (usually included in Python standard library)
- 以下Python标准库：  
  The following Python standard libraries:
  - subprocess
  - threading
  - webbrowser

## 使用方法 Usage

1. 输入包名到文本框中  
   Enter the package name in the text box
2. 选择镜像源（默认：阿里云）  
   Select a mirror source (default: Aliyun)
3. 点击对应功能按钮：  
   Click the corresponding function button:
   - **安装 Install**：从选定源安装最新版本  
     Install the latest version from the selected source
   - **升级 Upgrade**：升级到最新版本  
     Upgrade to the latest version
   - **卸载 Uninstall**：完全移除包  
     Completely remove the package
   - **包详情 Details**：在浏览器打开PyPI中有关您在输入框输入的软件包页面  
     Open the PyPI page of the package you entered in the entry
   - **关于 About**：查看版本信息和源代码  
     View version information and source code

## 技术细节 Technical

- 使用 `subprocess` 模块调用系统pip命令  
  Use the `subprocess` module to call system pip commands
- 通过 `threading` 实现异步操作  
  Implement asynchronous operations through `threading`
- 自动捕获并显示命令输出  
  Automatically capture and display command output
- 错误处理机制：  
  Error handling mechanism:
  - 捕获CalledProcessError  
    Catch CalledProcessError
  - 显示标准错误输出  
    Display standard error output
  - 防止重复点击  
    Prevent duplicate clicks

## 支持的镜像源 Supported Sources

| 名称 Name       | URL                                      |
|---------------|------------------------------------------|
| 阿里云 Aliyun    | https://mirrors.aliyun.com/pypi/simple   |
| PyPI          | https://pypi.org/simple                  |
| 清华大学 Tsinghua | https://pypi.tuna.tsinghua.edu.cn/simple |

## 开发贡献 Contributing

欢迎提交 `Issue` 和 `Pull Request`：  
Welcome to submit `Issue` and `Pull Request`:
1. `Fork` 仓库 `Fork` the repository
2. 创建特性分支 Create a feature branch 
    ```bash
    git checkout -b feature/new-feature
    ```
3. 提交修改 Commit your changes
    ```bash
    git commit -am 'Add new feature'
    ```
4. 推送分支 Push the branch
    ```bash
    git push origin feature/new-feature
    ```
5. 新建 `Pull Request` Create a new `Pull Request`
