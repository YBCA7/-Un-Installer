import webbrowser
from subprocess import Popen, PIPE
from sys import executable
from threading import Thread


class PackageManager:
    """Python包管理命令执行核心
    Core executor for Python package management commands
    
    职责：
    - 执行pip安装/升级/卸载操作
    - 实时捕获并转发命令输出
    - 提供PyPI包详情页跳转
    ---
    Responsibilities:
    - Execute pip install/upgrade/uninstall operations
    - Capture and forward command output in real-time
    - Provide PyPI package details page redirection
    """

    def __init__(self, ui_callback):
        self.pip_command_prefix = [executable, "-m", "pip"]
        self.ui_callback = ui_callback

    def execute(self, command, package_name, source_url=None):
        """执行pip命令主入口 / Main entry for pip command execution
        
        Args:
            command (str): 操作类型 ['install'|'upgrade'|'uninstall'] / 
                          Command type ['install'|'upgrade'|'uninstall']
            package_name (str): 目标包名称 / Target package name
            source_url (str, optional): 镜像源URL / Mirror source URL
        
        Raises:
            ValueError: 当传入无效命令类型时 / When invalid command type is passed
        """

        if command == "install":
            full_command = self.pip_command_prefix + [
                "install", "-i", source_url, package_name
            ]
        elif command == "upgrade":
            full_command = self.pip_command_prefix + [
                "install", "--upgrade", package_name, "-i", source_url
            ]
        elif command == "uninstall":
            full_command = self.pip_command_prefix + [
                "uninstall", package_name, "-y"
            ]
        else:
            raise ValueError("Invalid command")

        with Popen(full_command, stdout=PIPE, stderr=PIPE, text=True,
                  bufsize=1, universal_newlines=True) as process:
            Thread(target=self._catch_output, args=(process,), daemon=True).start()
            process.wait()
            if process.returncode != 0:
                err = process.stderr.read()
                if err:
                    self.ui_callback('show_error', err)

    def _catch_output(self, process):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.ui_callback('show_output', output)
        process.stdout.close()

    def open_package_details(self, package_name):
        webbrowser.open(f"https://pypi.org/project/{package_name}/")
