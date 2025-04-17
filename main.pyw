from tkinter import Tk
from os.path import exists
from data import dump_default_data
from ui import App


if __name__ == "__main__":
	if not exists('data.json'):
		dump_default_data()
	main_window = Tk()
	App(main_window)
	main_window.mainloop()
