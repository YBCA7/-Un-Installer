from tkinter import Tk
from tkinter.ttk import Label, Button, Entry
from os import system
from sys import prefix
from threading import Thread

r = Tk()
r.title('-Un-installer')
Label(text="需要装卸的包  Name of Package: ").grid(row=0, column=0)
e = Entry(width=50)
e.grid(row=0, column=1)
path = prefix + "\\Scripts\\pip.exe"

insb = Button(text="安装  Install", width=61)
insb.grid(row=1, columnspan=2)
unib = Button(text="卸载（在弹出窗口中输y）  Uninstall", width=61)
unib.grid(row=2, columnspan=2)


def inst():
    insb.config(state="disabled", text="执行中  Executing…")
    unib.config(state="disabled")
    system(path + " install " + e.get())
    insb.config(state="normal", text="安装  Install")
    unib.config(state="normal")


def uninst():
    insb.config(state="disabled")
    unib.config(state="disabled", text="执行中  Executing…")
    system(path + " uninstall " + e.get())
    insb.config(state="normal")
    unib.config(state="normal", text="卸载（请在弹出窗口中输Y）  Uninstall")


def install():
    thread = Thread(target=inst)
    thread.start()


def uninstall():
    thread = Thread(target=uninst)
    thread.start()


insb.config(command=install)
unib.config(command=uninstall)
r.mainloop()
