from tkinter import Tk, Toplevel, Text, Scrollbar
from tkinter.ttk import Label, Button, Entry, Combobox
from tkinter.messagebox import showerror
from subprocess import Popen, PIPE
from sys import executable
from threading import Thread
import webbrowser


class App:
    def __init__(self, window):
        self.main_window = window
        self.main_window.title('-Un-Installer')
        self.main_window.resizable(False, False)

        self.sources = {
            '阿里云  Aliyun': 'https://mirrors.aliyun.com/pypi/simple',
            'PyPI': 'https://pypi.org/simple',
            '清华大学  Tsinghua University': 'https://pypi.tuna.tsinghua.edu.cn/simple'
        }
        self.pip_command_prefix = [executable, "-m", "pip"]

        self.buttons = {
            "install":Button(text="安装  Install", width=79),
            "upgrade":Button(text="升级  Upgrade", width=79),
            "uninstall":Button(text="卸载  Uninstall", width=79)
        }
        self.entry = Entry(width=40)
        self.source_combobox = Combobox(width=37)
        self.output_text = Text(width=62, height=10, font="Consolas")
        self.scrollbar = Scrollbar(command=self.output_text.yview)
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        self.setup_widgets()

    def setup_widgets(self):
        Label(text="需要装卸的包  Name of Package: ").grid(row=0, column=0, pady=5)
        self.entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        Label(text="下载源  Source: ").grid(row=1, column=0, pady=5)

        self.source_combobox.grid(row=1, column=1, pady=5, columnspan=2)
        self.source_combobox['state'] = 'readonly'
        self.source_combobox['values'] = tuple(self.sources.keys())
        self.source_combobox.set(tuple(self.sources.keys())[0])

        self.buttons["install"].config(command=lambda: Thread(target=self.install).start())
        self.buttons["upgrade"].config(command=lambda: Thread(target=self.upgrade).start())
        self.buttons["uninstall"].config(command=lambda: Thread(target=self.uninstall).start())

        self.buttons["install"].grid(row=2, columnspan=3, pady=5)
        self.buttons["upgrade"].grid(row=3, columnspan=3, pady=5)
        self.buttons["uninstall"].grid(row=4, columnspan=3, pady=5)

        Button(text="该软件包详情  Details of the Package",
               command=self.show_package_details, width=79).grid(row=5, columnspan=3, pady=5)
        Button(text="关于  About",
               command=self.show_about_window, width=79).grid(row=6, columnspan=3, pady=5)

        self.output_text.insert('end', """开始执行命令后，这里将显示输出。
After the command starts executing, the output will be displayed here.""")
        self.output_text.grid(row=7, columnspan=2)
        self.scrollbar.grid(row=7, column=2, sticky='ns')

    def execute(self, command):
        for button in self.buttons:
            button.config(state="disabled")
        self.output_text.delete(1.0, 'end')

        def show_output(current_process):
            while True:
                output = current_process.stdout.readline()
                if output == '' and current_process.poll() is not None:
                    break
                if output:
                    self.output_text.config(state="normal")
                    self.output_text.insert('end', output)
                    self.output_text.see('end')
                    self.output_text.config(state="disabled")
            current_process.stdout.close()

        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE,
                            text=True, bufsize=1, universal_newlines=True)
            Thread(target=show_output, args=(process,), daemon=True).start()
            process.wait()
            if process.returncode != 0:
                err = process.stderr.read()
                if err:
                    self.output_text.insert('end', err)
                    self.output_text.see('end')
                    showerror('错误  Error', err)
        except Exception as e:
            self.output_text.insert('end', f"出现了一些错误  There were some errors: {str(e)}\n")
            self.output_text.see('end')
            showerror('错误  Error', f"出现了一些错误  There were some errors: {str(e)}")
        finally:
            for button in self.buttons:
                button.config(state="normal")

    def install(self):
        self.install_button.config(text="执行中  Executing…")
        self.execute(self.pip_command_prefix + [
            "install", "-i", self.sources[self.source_combobox.get()], self.entry.get()
        ])
        self.install_button.config(text="安装  Install")

    def upgrade(self):
        self.update_button.config(text="执行中  Executing…")
        self.execute(
            self.pip_command_prefix + [
                "install", "--upgrade", self.entry.get(), "-i",
                self.sources[self.source_combobox.get()]
            ]
        )
        self.update_button.config(text="升级  Upgrade")

    def uninstall(self):
        self.uninstall_button.config(text="执行中  Executing…")
        self.execute(self.pip_command_prefix + ["uninstall", self.entry.get(), "-y"])
        self.uninstall_button.config(text="卸载  Uninstall")

    def show_about_window(self):
        about_window = Toplevel(self.main_window)
        about_window.grab_set()
        about_window.focus_set()
        about_window.title("关于  About")
        about_window.resizable(False, False)
        Label(about_window, text="-Un-Installer", font=("Consolas", 20)).pack(padx=5, pady=5)
        Label(about_window, text="Version 6.2").pack(padx=5, pady=5)
        Button(about_window, text="源代码仓库  Source Code Repository",
               command=lambda: webbrowser.open("https://github.com/YBCA7/-Un-Installer"),
               width=50).pack(padx=5, pady=5)
        Button(about_window, text="关闭  Close",
               command=about_window.destroy, width=50).pack(padx=5, pady=5)

    def show_package_details(self):
        webbrowser.open(f"https://pypi.org/project/{self.entry.get()}/")


if __name__ == "__main__":
    main_window = Tk()
    App(main_window)
    main_window.mainloop()
