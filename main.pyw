from tkinter import Tk
from tkinter.ttk import Label, Button, Entry, Combobox
from tkinter.messagebox import showinfo, showerror
from subprocess import run, CalledProcessError
from sys import prefix
from threading import Thread


r = Tk()
r.title('-Un-installer')
r.resizable(False, False)

Label(text="需要装卸的包  Name of Package: ").grid(row=0, column=0, padx=5, pady=5)
e = Entry(width=50)
e.grid(row=0, column=1, padx=5, pady=5)
Label(text="下载源  Source: ").grid(row=1, column=0, padx=5, pady=5)
src_b = Combobox(width=48)
src_b.grid(row=1, column=1, padx=5, pady=5)
src_b['state'] = 'readonly'
src_b['values'] = ('清华大学  Tsinghua University', '阿里云  Aliyun', 'PyPI')
src_b.set('清华大学  Tsinghua University')

sources = {
    '清华大学  Tsinghua University':'https://pypi.tuna.tsinghua.edu.cn/simple',
    '阿里云  Aliyun':'https://mirrors.aliyun.com/pypi/simple',
    'PyPI':'https://pypi.org/simple'
}
path = prefix + "\\Scripts\\pip.exe"

ins_b = Button(text="安装  Install", width=78)
ins_b.grid(row=2, columnspan=2, padx=5, pady=5)
uni_b = Button(text="卸载  Uninstall", width=78)
uni_b.grid(row=3, columnspan=2, padx=5, pady=5)


def execute(command):
    """
    Execute a command and display the output, and capture and display error messages when execution fails.
    执行一条指令并显示输出，且在执行出错时捕获并显示错误信息。
    """
    try:
        showinfo('Output', run(command, capture_output=True, text=True, check=True).stdout)
    except CalledProcessError as error:
        showerror('Error', error.stderr)


def inst():
    ins_b.config(state="disabled", text="执行中  Executing…")
    uni_b.config(state="disabled")
    execute(f"{path} install -i {sources[src_b.get()]} {e.get()}")
    ins_b.config(state="normal", text="安装  Install")
    uni_b.config(state="normal")


def un_inst():
    ins_b.config(state="disabled")
    uni_b.config(state="disabled", text="执行中  Executing…")
    execute(f"{path} uninstall {e.get()} -y")
    ins_b.config(state="normal")
    uni_b.config(state="normal", text="卸载  Uninstall")


def install():
    thread = Thread(target=inst)
    thread.start()


def uninstall():
    thread = Thread(target=un_inst)
    thread.start()


ins_b.config(command=install)
uni_b.config(command=uninstall)
r.mainloop()
