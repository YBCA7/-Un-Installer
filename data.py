from json import dump


def dump_default_data():
    with open('data.json', 'w') as f:
        dump({
            "LANGUAGES": {
                "English": {
                    "app_title": "-Un-Installer", "package_label": "Package Name: ",
                    "source_label": "Source: ", "install_btn": "Install",
                    "upgrade_btn": "Upgrade", "uninstall_btn": "Uninstall",
                    "details_btn": "Details of the Package", "about_btn": "About",
                    "initial_output": "After the command starts executing, the output will be displayed here.",
                    "error_title": "Error", "error_msg": "There were some errors: {error}",
                    "executing_text": "Executing...", "about_title": "About",
                    "version_text": "Version 6.3", "source_code_btn": "Source Code Repository",
                    "close_btn": "Close", "settings_btn": "Settings",
                    "language_label": "Language: ", "default_source_label": "Default Source: ",
                    "save_btn": "Confirm", "cancel_btn": "Cancel",
                    "restart_prompt": "Please restart the application to apply changes."
                },
                "中文": {
                    "app_title": "-Un-Installer", "package_label": "需要装卸的包: ",
                    "source_label": "下载源: ", "install_btn": "安装",
                    "upgrade_btn": "升级", "uninstall_btn": "卸载",
                    "details_btn": "该软件包详情", "about_btn": "关于",
                    "initial_output": "开始执行命令后，这里将显示输出。",
                    "error_title": "错误", "error_msg": "出现了一些错误: {error}",
                    "executing_text": "执行中...", "about_title": "关于",
                    "version_text": "版本 6.3", "source_code_btn": "源代码仓库",
                    "close_btn": "关闭", "settings_btn": "设置",
                    "language_label": "语言: ", "default_source_label": "默认下载源: ",
                    "save_btn": "确定", "cancel_btn": "取消",
                    "restart_prompt": "请重启程序以应用更改。"
                }
            },
            "SOURCES": {
                "Aliyun": "https://mirrors.aliyun.com/pypi/simple",
                "PyPI": "https://pypi.org/simple",
                "Tsinghua University": "https://pypi.tuna.tsinghua.edu.cn/simple"
            },
            "settings": {
                "language": "English", "default_source": "PyPI"
            }
        }, f, indent=4)
