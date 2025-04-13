from json import dump, load


DEFAULT_DATA = {
    "LANGUAGES": {
        "English": {
            "app_title": "-Un-Installer", "package_label": "Package Name: ",
            "source_label": "Source: ", "install_btn": "Install",
            "upgrade_btn": "Upgrade", "uninstall_btn": "Uninstall",
            "details_btn": "Details of the Package", "about_btn": "About",
            "initial_output": "After the command starts executing, " +
                              "the output will be displayed here.",
            "error_title": "Error", "error_msg": "There were some errors: {error}",
            "executing_text": "Executing...", "about_title": "About",
            "version_text": "Version 0.7.0", "source_code_btn": "Source Code Repository",
            "close_btn": "Close", "settings_btn": "Settings",
            "language_label": "Language: ", "default_source_label": "Default Source: ",
            "save_btn": "Confirm", "cancel_btn": "Cancel",
            "restart_prompt": "Please restart the application to apply changes.",
            "confirm_exit_text": "A command is executing. Are you sure you want to quit?",
            "file_label": "To batch manage the package in files\nformat that complies " +
                          "with requirements.txt.",
            "file_btn": "Add Files",
            "batch_label": "Batch Operations"
        },
        "中文": {
            "app_title": "-Un-Installer", "package_label": "需要装卸的包: ",
            "source_label": "下载源: ", "install_btn": "安装",
            "upgrade_btn": "升级", "uninstall_btn": "卸载",
            "details_btn": "该软件包详情", "about_btn": "关于",
            "initial_output": "开始执行命令后，这里将显示输出。",
            "error_title": "错误", "error_msg": "出现了一些错误: {error}",
            "executing_text": "执行中...", "about_title": "关于",
            "version_text": "版本 0.7.0", "source_code_btn": "源代码仓库",
            "close_btn": "关闭", "settings_btn": "设置",
            "language_label": "语言: ", "default_source_label": "默认下载源: ",
            "save_btn": "确定", "cancel_btn": "取消",
            "restart_prompt": "请重启程序以应用更改。" ,
            "confirm_exit_text": "有指令正在执行，确定要退出吗？",
            "file_label": "点击下方按钮，以格式符合\n" +
                          "requirements.txt 的文件批量管理包。",
            "file_btn": "添加文件",
            "batch_label": "批量操作"
        }
    },
    "SOURCES": {
        "阿里云": "https://mirrors.aliyun.com/pypi/simple",
        "PyPI": "https://pypi.org/simple",
        "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple"
    },
    "settings": {
        "language": "English", "default_source": "PyPI"
    }
}


def dump_default_data():
    with open('data.json', 'w', encoding='utf-8') as file_to_dump:
        dump(DEFAULT_DATA, file_to_dump, indent=4)


def load_data():
    with open('data.json', 'r', encoding='utf-8') as file_to_load:
        return load(file_to_load)


def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as file_to_save:
        dump(data, file_to_save, indent=4)
