from tkinter import Tk, Toplevel
from tkinter.ttk import Label, Button, Entry, Combobox
from tkinter.messagebox import showinfo, showerror
from subprocess import run, CalledProcessError
from sys import prefix
from threading import Thread
import webbrowser


class Un_Installer_App:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title('-Un-Installer')
        self.main_window.resizable(False, False)

        self.sources = {
            '阿里云  Aliyun': 'https://mirrors.aliyun.com/pypi/simple',
            'PyPI': 'https://pypi.org/simple',
            '清华大学  Tsinghua University': 'https://pypi.tuna.tsinghua.edu.cn/simple'
        }
        self.path = prefix + "\\Scripts\\pip.exe"

        self.create_widgets()
        self.setup_buttons()

    def create_widgets(self):
        Label(text="需要装卸的包  Name of Package: ").grid(row=0, column=0, padx=5, pady=5)
        self.entry = Entry(width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        Label(text="下载源  Source: ").grid(row=1, column=0, padx=5, pady=5)
        self.source_combobox = Combobox(width=48)
        self.source_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.source_combobox['state'] = 'readonly'
        self.source_combobox['values'] = tuple(self.sources.keys())
        self.source_combobox.set(tuple(self.sources.keys())[0])

        self.install_button = Button(text="安装  Install", width=78)
        self.install_button.grid(row=2, columnspan=2, padx=5, pady=5)

        self.update_button = Button(text="升级  Update", width=78)
        self.update_button.grid(row=3, columnspan=2, padx=5, pady=5)

        self.uninstall_button = Button(text="卸载  Uninstall", width=78)
        self.uninstall_button.grid(row=4, columnspan=2, padx=5, pady=5)

        Button(text="该软件包详情  Details of the Package",
               command=self.show_package_details, width=78).grid(row=5, columnspan=2, padx=5, pady=5)
        Button(text="关于  About", command=self.show_about_window, width=78).grid(row=6, columnspan=2, padx=5, pady=5)

    def setup_buttons(self):
        self.install_button.config(command=lambda: Thread(target=self.install).start())
        self.update_button.config(command=lambda: Thread(target=self.update).start())
        self.uninstall_button.config(command=lambda: Thread(target=self.uninstall).start())

    def execute(self, command):
        for button in (self.install_button, self.update_button, self.uninstall_button):
            button.config(state="disabled")
        try:
            output = run(command, capture_output=True, text=True, check=True).stdout
            if output:
                showinfo('输出  Output', output)
            else:
                showinfo('输出  Output', """命令已执行完毕，退出代码为0。
The command has been executed and the exit code is 0.""")
        except CalledProcessError as error:
            err = error.stderr
            if err:
                showerror('错误  Error', error.stderr)
            else:
                showerror('错误  Error', """出现了一些错误，很有可能是因为您提前关闭了命令窗口。
Some errors occurred, which are very likely due to the fact that you closed the command window prematurely.""")
        finally:
            for button in (self.install_button, self.update_button, self.uninstall_button):
                button.config(state="normal")

    def install(self):
        self.install_button.config(text="执行中  Executing…")
        self.execute(f"{self.path} install -i {self.sources[self.source_combobox.get()]} {self.entry.get()}")
        self.install_button.config(text="安装  Install")

    def update(self):
        self.update_button.config(text="执行中  Executing…")
        self.execute(f"{self.path} install --upgrade {self.entry.get()} -i {self.sources[self.source_combobox.get()]}")
        self.update_button.config(text="升级  Update")

    def uninstall(self):
        self.uninstall_button.config(text="执行中  Executing…")
        self.execute(f"{self.path} uninstall {self.entry.get()} -y")
        self.uninstall_button.config(text="卸载  Uninstall")

    def show_about_window(self):
        about_window = Toplevel(self.main_window)
        about_window.grab_set()
        about_window.title("关于  About")
        about_window.resizable(False, False)
        Label(about_window, text="-Un-Installer", font=("Consolas", 20)).pack(pady=5)
        Label(about_window, text="Version 5.0").pack(pady=5)
        Button(about_window, text="源代码仓库  Source Code Repository",
               command=lambda: webbrowser.open("https://github.com/YBCA7/-Un-installer"), width=50).pack(pady=5)
        Button(about_window, text="关闭  Close",
               command=about_window.destroy, width=50).pack(pady=5)

    def show_package_details(self):
        webbrowser.open(f"https://pypi.org/project/{self.entry.get()}/")


if __name__ == "__main__":
    main_window = Tk()  # 将 root 改为更具描述性的名称
    app = Un_Installer_App(main_window)
    main_window.mainloop()
