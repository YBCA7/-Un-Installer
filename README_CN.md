# -Un-Installer

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-Apache--2.0-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![Version](https://img.shields.io/badge/Version-1.0.0-lightgrey)

[English](README.md)

基于 `Tkinter` 的 **Python包管理图形界面工具**，支持多镜像源选择和批量操作。

## 功能特性

- 🚀 一键安装/升级/卸载Python包
- 🌍 支持多个镜像源（阿里云/PyPI/清华大学等）
- 📦 自动跳转PyPI包详情页面
- 📁 从requirements.txt文件批量操作
- ⚙️ 多线程执行防止界面冻结
- 🌐 中英双语界面
- 📜 实时命令输出显示
- 🔒 执行期间按钮禁用防止误操作
- 🖥️ 控制台风格输出显示（等宽字体）
- ⚙️ 可配置语言和默认镜像源

## 安装要求

- Python 3.6 以上版本
- Tkinter（通常包含在Python标准库中）
- 需要以下Python标准库：
  - `subprocess`
  - `threading`
  - `webbrowser`
  - `tkinter`
  - `tkinter.ttk`

## 使用方法

1. 在文本框中输入包名（或选择文件进行批量操作）
2. 选择镜像源（默认：PyPI）
3. 点击对应功能按钮：
   - **安装**：从选定源安装最新版本
   - **升级**：升级到最新版本
   - **卸载**：完全移除包
   - **详情**：在浏览器打开PyPI包详情页面
   - **设置**：更改语言和默认镜像源
   - **关于**：查看版本信息和源代码
4. 在下方输出框查看实时执行结果

## 技术细节

- 使用 `subprocess.Popen` 调用系统pip命令
- 通过 `threading.Thread` 实现异步操作
- 自动捕获并显示命令输出
- 使用等宽字体 `Consolas` 显示输出
- 错误处理机制：
  - 捕获所有异常并显示错误对话框
  - 显示标准错误输出
  - 执行期间禁用所有操作按钮
- 使用 `Toplevel` 创建关于窗口和设置窗口
- 使用现代 `ttk` 主题控件
- 配置数据持久化存储

## 支持的镜像源

| 名称                | URL                                      |
|---------------------|------------------------------------------|
| 阿里云             | https://mirrors.aliyun.com/pypi/simple   |
| PyPI               | https://pypi.org/simple                  |
| 清华大学           | https://pypi.tuna.tsinghua.edu.cn/simple |

您可以通过修改 `data.json` 添加自定义源。

## 界面结构

```
[包名输入框] [镜像源下拉框]

[安装按钮]     [升级按钮]
[卸载按钮]     [详情按钮]
[设置按钮]     [关于按钮]

[批量操作面板]
[文件列表]     [添加文件按钮]

[输出文本框]
```

## 开发贡献

欢迎提交 `Issue` 和 `Pull Request`：

1. `Fork` 本仓库
2. 创建特性分支 
    ```bash
    git checkout -b feature/new-feature
    ```
3. 提交修改
    ```bash
    git commit -am '添加新功能'
    ```
4. 推送分支
    ```bash
    git push origin feature/new-feature
    ```
5. 新建 `Pull Request`
