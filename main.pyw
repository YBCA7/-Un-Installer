from tkinter import Tk, Toplevel, Text, Scrollbar
from tkinter.ttk import Label, Button, Entry, Combobox
from tkinter.messagebox import showerror, showinfo
from subprocess import Popen, PIPE
from sys import executable
from threading import Thread
from json import load, dump
from os.path import exists
import webbrowser


class App:
    def __init__(self, window):
        self.load_data()
        self.main_window = window
        self.main_window.title(self.tr('app_title'))
        self.main_window.resizable(False, False)

        self.pip_command_prefix = [executable, "-m", "pip"]
        
        self.widgets = {
            "buttons": {
                "install": Button(text=self.tr('install_btn'), width=79),
                "upgrade": Button(text=self.tr('upgrade_btn'), width=79),
                "uninstall": Button(text=self.tr('uninstall_btn'), width=79)
            },
            "entry": Entry(width=40),
            "source_combobox": Combobox(width=37),
            "output": {
                "text": Text(width=80, height=10, font=("Consolas", 10)),
                "scrollbar": Scrollbar()
            }
        }

        self.setup_widgets()
    
    def load_data(self):
        with open('data.json', 'r') as f:
            data = load(f)
        self.LANGUAGES = data['LANGUAGES']
        self.SOURCES = data['SOURCES']
        self.settings = data['settings']
        self.lang = self.settings['language']

    def save_data(self):
        with open('data.json', 'w') as f:
            dump({
                'LANGUAGES': self.LANGUAGES,
                'SOURCES': self.SOURCES,
                'settings': self.settings
            }, f, indent=4)

    def tr(self, key):
        return self.LANGUAGES[self.lang].get(key, key)

    def setup_widgets(self):
        Label(text=self.tr('package_label')).grid(row=0, column=0, pady=5)
        self.widgets["entry"].grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        
        Label(text=self.tr('source_label')).grid(row=1, column=0, pady=5)
        self.widgets["source_combobox"].grid(row=1, column=1, pady=5, columnspan=2)
        self.widgets["source_combobox"]['state'] = 'readonly'
        self.widgets["source_combobox"]['values'] = tuple(self.SOURCES.keys())
        self.widgets["source_combobox"].set(self.settings['default_source'])

        self.widgets["buttons"]["install"].config(command=lambda: Thread(
            target=self.execute_pip_command, args=("install",)).start())
        self.widgets["buttons"]["upgrade"].config(command=lambda: Thread(
            target=self.execute_pip_command, args=("upgrade",)).start())
        self.widgets["buttons"]["uninstall"].config(command=lambda: Thread(
            target=self.execute_pip_command, args=("uninstall",)).start())

        self.widgets["buttons"]["install"].grid(row=2, columnspan=3, pady=5)
        self.widgets["buttons"]["upgrade"].grid(row=3, columnspan=3, pady=5)
        self.widgets["buttons"]["uninstall"].grid(row=4, columnspan=3, pady=5)

        Button(text=self.tr('details_btn'),
               command=lambda: webbrowser.open(f"https://pypi.org/project/{self.widgets['entry'].get()}/"),
               width=79).grid(row=5, columnspan=3, pady=5)
        Button(text=self.tr('settings_btn'),
               command=self.show_settings_window, width=79).grid(row=6, columnspan=3, pady=5)
        Button(text=self.tr('about_btn'),
               command=self.show_about_window, width=79).grid(row=7, columnspan=3, pady=5)

        self.show(self.tr('initial_output'))
        self.widgets["output"]["text"].grid(row=8, columnspan=2)
        self.widgets["output"]["scrollbar"].grid(row=8, column=2, sticky='ns')
        self.widgets["output"]["scrollbar"].config(command=self.widgets["output"]["text"].yview)
        self.widgets["output"]["text"].config(yscrollcommand=self.widgets["output"]["scrollbar"].set)

    def show(self, text):
        self.widgets["output"]["text"].config(state="normal")
        self.widgets["output"]["text"].insert('end', text)
        self.widgets["output"]["text"].see('end')
        self.widgets["output"]["text"].config(state="disabled")

    def execute(self, command):
        for button in self.widgets["buttons"].values():
            button.config(state="disabled")

        self.widgets["output"]["text"].config(state="normal")
        self.widgets["output"]["text"].delete(1.0, 'end')
        self.widgets["output"]["text"].config(state="disabled")

        def catch_and_show_output(current_process):
            while True:
                output = current_process.stdout.readline()
                if output == '' and current_process.poll() is not None:
                    break
                if output:
                    self.show(output)
            current_process.stdout.close()

        try:
            with Popen(command, stdout=PIPE, stderr=PIPE, text=True,
                       bufsize=1, universal_newlines=True) as process:
                Thread(target=catch_and_show_output, args=(process,), daemon=True).start()
                process.wait()
                if process.returncode != 0:
                    err = process.stderr.read()
                    if err:
                        self.show(err)
                        showerror(self.tr('error_title'), err)
        except Exception as e:
            self.show(self.tr('error_msg').format(error=str(e)) + "\n")
            showerror(self.tr('error_title'), self.tr('error_msg').format(error=str(e)))
        finally:
            for button in self.widgets["buttons"].values():
                button.config(state="normal")

    def execute_pip_command(self, command):
        self.widgets["buttons"][command].config(text=f"{self.tr('executing_text')}")
        
        if command == "install":
            self.execute(self.pip_command_prefix + [
                "install", "-i", self.SOURCES[self.widgets["source_combobox"].get()], self.widgets["entry"].get()
            ])
        elif command == "upgrade":
            self.execute(self.pip_command_prefix + [
                "install", "--upgrade", self.widgets["entry"].get(), "-i",
                self.SOURCES[self.widgets["source_combobox"].get()]
            ])
        elif command == "uninstall":
            self.execute(self.pip_command_prefix + ["uninstall", self.widgets["entry"].get(), "-y"])

        self.widgets["buttons"][command].config(text=self.tr(command + '_btn'))

    def show_about_window(self):
        about_window = Toplevel(self.main_window)
        about_window.grab_set()
        about_window.focus_set()
        about_window.title(self.tr('about_title'))
        about_window.resizable(False, False)
        
        Label(about_window, text="-Un-Installer", font=("Consolas", 20)).pack(padx=5, pady=5)
        Label(about_window, text=self.tr('version_text')).pack(padx=5, pady=5)
        
        Button(about_window, text=self.tr('source_code_btn'),
               command=lambda: webbrowser.open("https://github.com/YBCA7/-Un-Installer"),
               width=50).pack(padx=5, pady=5)
        Button(about_window, text=self.tr('close_btn'),
               command=about_window.destroy, width=50).pack(padx=5, pady=5)

    def show_settings_window(self):
        settings_window = Toplevel(self.main_window)
        settings_window.grab_set()
        settings_window.focus_set()
        settings_window.title(self.tr('settings_btn'))
        settings_window.resizable(False, False)

        Label(settings_window, text=self.tr('language_label')).grid(row=0, column=0, padx=5, pady=5)
        language_combobox = Combobox(settings_window, width=20, state='readonly')
        language_combobox.grid(row=0, column=1, padx=5, pady=5)
        language_combobox['values'] = tuple(self.LANGUAGES.keys())
        language_combobox.set(self.settings['language'])

        Label(settings_window, text=self.tr('default_source_label')).grid(row=1, column=0, padx=5, pady=5)
        source_combobox = Combobox(settings_window, width=20, state='readonly')
        source_combobox.grid(row=1, column=1, padx=5, pady=5)
        source_combobox['values'] = tuple(self.SOURCES.keys())
        source_combobox.set(self.settings['default_source'])

        def save_settings():
            self.settings['language'] = language_combobox.get()
            self.settings['default_source'] = source_combobox.get()
            self.save_data()
            showinfo(self.tr('settings_btn'), self.tr('restart_prompt'))
            settings_window.destroy()

        Button(settings_window, text=self.tr('save_btn'),
               command=save_settings, width=20).grid(row=2, column=0, padx=5, pady=5)
        Button(settings_window, text=self.tr('cancel_btn'),
               command=settings_window.destroy, width=20).grid(row=2, column=1, padx=5, pady=5)


if __name__ == "__main__":
    if not exists('data.json'):
        with open('data.json', 'w') as f:
            dump({
                "LANGUAGES": {
                    "English": {
                        "app_title": "-Un-Installer",
                        "package_label": "Package Name: ",
                        "source_label": "Source: ",
                        "install_btn": "Install",
                        "upgrade_btn": "Upgrade",
                        "uninstall_btn": "Uninstall",
                        "details_btn": "Details of the Package",
                        "about_btn": "About",
                        "initial_output": "After the command starts executing, the output will be displayed here.",
                        "error_title": "Error",
                        "error_msg": "There were some errors: {error}",
                        "executing_text": "Executing...",
                        "about_title": "About",
                        "version_text": "Version 6.3",
                        "source_code_btn": "Source Code Repository",
                        "close_btn": "Close",
                        "settings_btn": "Settings",
                        "language_label": "Language: ",
                        "default_source_label": "Default Source: ",
                        "save_btn": "Save",
                        "cancel_btn": "Cancel",
                        "restart_prompt": "Please restart the application to apply changes."
                    },
                    "中文": {
                        "app_title": "-Un-Installer",
                        "package_label": "需要装卸的包: ",
                        "source_label": "下载源: ",
                        "install_btn": "安装",
                        "upgrade_btn": "升级",
                        "uninstall_btn": "卸载",
                        "details_btn": "该软件包详情",
                        "about_btn": "关于",
                        "initial_output": "开始执行命令后，这里将显示输出。",
                        "error_title": "错误",
                        "error_msg": "出现了一些错误: {error}",
                        "executing_text": "执行中...",
                        "about_title": "关于",
                        "version_text": "版本 6.3",
                        "source_code_btn": "源代码仓库",
                        "close_btn": "关闭",
                        "settings_btn": "设置",
                        "language_label": "语言: ",
                        "default_source_label": "默认下载源: ",
                        "save_btn": "确定",
                        "cancel_btn": "取消",
                        "restart_prompt": "请重启程序以应用更改。"
                    }
                },
                "SOURCES": {
                    "Aliyun": "https://mirrors.aliyun.com/pypi/simple",
                    "PyPI": "https://pypi.org/simple",
                    "Tsinghua University": "https://pypi.tuna.tsinghua.edu.cn/simple"
                },
                "settings": {
                    "language": "English",
                    "default_source": "PyPI"
                }
            }, f, indent=4)

    main_window = Tk()
    App(main_window)
    main_window.mainloop()
