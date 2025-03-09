from tkinter import Tk, Toplevel
from tkinter.ttk import Label, Button, Entry, Combobox
from tkinter.messagebox import showinfo, showerror
from subprocess import run, CalledProcessError
from sys import prefix
from threading import Thread
from webbrowser import open


r = Tk()
r.title('-Un-installer')
r.resizable(False, False)

sources = {
    '阿里云  Aliyun':'https://mirrors.aliyun.com/pypi/simple',
    'PyPI':'https://pypi.org/simple',
    '清华大学  Tsinghua University':'https://pypi.tuna.tsinghua.edu.cn/simple'
}
path = prefix + "\\Scripts\\pip.exe"

Label(text="需要装卸的包  Name of Package: ").grid(row=0, column=0, padx=5, pady=5)
e = Entry(width=50)
e.grid(row=0, column=1, padx=5, pady=5)
Label(text="下载源  Source: ").grid(row=1, column=0, padx=5, pady=5)
src_b = Combobox(width=48)
src_b.grid(row=1, column=1, padx=5, pady=5)
src_b['state'] = 'readonly'
source_names = tuple(sources.keys())
src_b['values'] = source_names
src_b.set(source_names[0])
ins_b = Button(text="安装  Install", width=78)
ins_b.grid(row=2, columnspan=2, padx=5, pady=5)
upd_b = Button(text="升级  Update", width=78)
upd_b.grid(row=3, columnspan=2, padx=5, pady=5)
uni_b = Button(text="卸载  Uninstall", width=78)
uni_b.grid(row=4, columnspan=2, padx=5, pady=5)


def execute(command):
    """
    Execute a command and display the output, and capture and display error messages when execution fails.
    执行一条指令并显示输出，且在执行出错时捕获并显示错误信息。
    """
    for button in (ins_b, upd_b, uni_b):
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
        for button in (ins_b, upd_b, uni_b):
            button.config(state="normal")


def install():
    ins_b.config(text="执行中  Executing…")
    execute(f"{path} install -i {sources[src_b.get()]} {e.get()}")
    ins_b.config(text="安装  Install")


def update():
    upd_b.config(text="执行中  Executing…")
    execute(f"{path} install --upgrade {e.get()} -i {sources[src_b.get()]}")
    upd_b.config(text="升级  Update")


def uninstall():
    uni_b.config(text="执行中  Executing…")
    execute(f"{path} uninstall {e.get()} -y")
    uni_b.config(text="卸载  Uninstall")


def thread_start(function):
    thread = Thread(target=function)
    thread.start()


def show_about_window():
    about_window = Toplevel(r)
    about_window.grab_set()
    about_window.title("关于  About")
    about_window.resizable(False, False)
    Label(about_window, text="-Un-installer", font=("Consolas", 20)).pack(pady=5)
    Label(about_window, text="Version 5.0").pack(pady=5)
    Button(about_window, text="源代码仓库  Source Code Repository",
           command=lambda: open("https://github.com/YBCA7/-Un-installer"), width=50).pack(pady=5)
    Button(about_window, text="关闭  Close",
           command=lambda: about_window.destroy, width=50).pack(pady=5)


Button(text="该软件包详情  Details of the Package",
       command=lambda: open(f"https://pypi.org/project/{e.get()}/"),
       width=78).grid(row=5, columnspan=2, padx=5, pady=5)
Button(text="关于  About", command=show_about_window, width=78).grid(row=6, columnspan=2, padx=5, pady=5)
ins_b.config(command=lambda: thread_start(install))
uni_b.config(command=lambda: thread_start(uninstall))
r.mainloop()
