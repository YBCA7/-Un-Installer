import webbrowser
from tkinter import Toplevel, Text, Scrollbar, Listbox, END
from tkinter.ttk import Label, Button, Entry, Combobox, LabelFrame
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.filedialog import askopenfilenames
from threading import Thread
from data import load_data, save_data
from commands import PackageManager


class App:
	"""
	Tkinter图形界面主类 / Main Tkinter GUI class
	
	功能特性 / Features:
	- 多语言支持 / Multilingual support
	- 镜像源选择 / Mirror source selection
	- 实时输出显示 / Real-time output display
	- 线程安全操作 / Thread-safe operations
	"""

	def __init__(self, window):
		data = load_data()
		self.languages = data['LANGUAGES']
		self.sources = data['SOURCES']
		self.settings = data['settings']
		self.lang = self.settings['language']

		self.main_window = window
		self.main_window.title(self.tr('app_title'))
		self.main_window.resizable(False, False)
		self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)

		self.package_manager = PackageManager(self.ui_callback)

		self.frames = {
			"single": LabelFrame(self.main_window,
				text=self.tr("single_label"), borderwidth=10),
			"batch": LabelFrame(self.main_window,
				text=self.tr("batch_label"), borderwidth=10)
		}
		self.widgets = {
			"buttons": {
				"install": Button(text=self.tr('install_btn'), width=79),
				"upgrade": Button(text=self.tr('upgrade_btn'), width=79),
				"uninstall": Button(text=self.tr('uninstall_btn'), width=79)
			},
			"entry": Entry(self.frames["single"], width=40),
			"source_combobox": Combobox(width=37),
			"file_label": Label(self.frames["batch"], text=self.tr('file_label')),
			"file_btn": Button(self.frames["batch"], text=self.tr('file_btn'),
							   width=36, command=self.open_file),
			"file_list": Listbox(self.frames["batch"], width=37, selectmode='multiple'),
			"file_x_scroll": Scrollbar(self.frames["batch"], orient="horizontal"),
			"file_y_scroll": Scrollbar(self.frames["batch"]),
			"output": {
				"text": Text(width=80, height=10, font=("Consolas", 10)),
				"scrollbar": Scrollbar()
			}
		}
		self.setup_widgets()

	def on_close(self):
		if self.package_manager.process:
			if askyesno(self.tr('app_title'),
						self.tr('confirm_exit_text')):
				self.package_manager.terminate()
				self.main_window.destroy()
		else:
			self.main_window.destroy()

	def ui_callback(self, action, *args):
		"""
		包管理器回调处理器 / Package manager callback handler
		
		Args:
			action (str): 操作类型 ['show_output'|'show_error'] / 
						 Action type ['show_output'|'show_error']
			*args: 可变参数 (输出内容/错误信息) / 
				   Variadic args (output content/error message)
		"""

		if action == 'show_output':
			self.main_window.after(0, lambda: self.show(args[0]))
		elif action == 'show_error':
			self.main_window.after(0, lambda: self.show(args[0]))
			self.main_window.after(0, lambda:
				showerror(self.tr('error_title'), args[0]))

	def tr(self, key):
		return self.languages[self.lang].get(key, key)

	def setup_widgets(self):
		Label(self.frames["single"], text=self.tr('package_label')).grid(row=0, column=0, pady=5)
		self.widgets["entry"].grid(row=0, column=1, padx=5, pady=5, columnspan=2)

		self.frames["single"].grid(row=1, rowspan=2, columnspan=2, padx=5, pady=5)
		Label(text=self.tr('source_label')).grid(row=0, column=0, pady=5)
		self.widgets["source_combobox"].grid(row=0, column=1, pady=5)
		self.widgets["source_combobox"]['state'] = 'readonly'
		self.widgets["source_combobox"]['values'] = tuple(self.sources.keys())
		self.widgets["source_combobox"].set(self.settings['default_source'])

		self.widgets["buttons"]["install"].config(
			command=lambda: Thread(target=self.execute_command, args=("install",)).start())
		self.widgets["buttons"]["upgrade"].config(
			command=lambda: Thread(target=self.execute_command, args=("upgrade",)).start())
		self.widgets["buttons"]["uninstall"].config(
			command=lambda: Thread(target=self.execute_command, args=("uninstall",)).start())

		self.widgets["buttons"]["install"].grid(row=0, column=3, columnspan=3, pady=5)
		self.widgets["buttons"]["upgrade"].grid(row=1, column=3, columnspan=3, pady=5)
		self.widgets["buttons"]["uninstall"].grid(row=2, column=3, columnspan=3, pady=5)

		Button(self.frames["single"], text=self.tr('details_btn'),
			   command=lambda: PackageManager.open_package_details(
				   self.widgets['entry'].get()),
			   width=77).grid(row=1, columnspan=2, padx=5, pady=5)
		Button(text=self.tr('settings_btn'), command=self.show_settings_window,
			   width=79).grid(row=4, column=3, columnspan=3, pady=5)
		Button(text=self.tr('about_btn'),
			   command=self.show_about_window, width=79).grid(row=5, column=3, columnspan=3, pady=5)

		self.frames["batch"].grid(row=3, rowspan=3, columnspan=3, padx=5, pady=5)
		self.widgets["file_list"].grid(row=0, column=0, rowspan=2)
		self.widgets["file_x_scroll"].grid(row=2, column=0, sticky='ew')
		self.widgets["file_x_scroll"].config(
			command=self.widgets["file_list"].xview)
		self.widgets["file_y_scroll"].grid(row=0, column=1, rowspan=2, sticky='ns')
		self.widgets["file_y_scroll"].config(
			command=self.widgets["file_list"].yview)
		self.widgets["file_list"].config(
			xscrollcommand=self.widgets["file_x_scroll"].set,
			yscrollcommand=self.widgets["file_y_scroll"].set)
		self.widgets["file_label"].grid(row=0, column=2, padx=10)
		self.widgets["file_btn"].grid(row=1, column=2, padx=10)

		self.show(self.tr('initial_output'))
		self.widgets["output"]["text"].grid(row=3, column=3, columnspan=2)
		self.widgets["output"]["scrollbar"].grid(row=3, column=5, sticky='ns')
		self.widgets["output"]["scrollbar"].config(
			command=self.widgets["output"]["text"].yview)
		self.widgets["output"]["text"].config(
			yscrollcommand=self.widgets["output"]["scrollbar"].set)

	def show(self, text):
		self.widgets["output"]["text"].config(state="normal")
		self.widgets["output"]["text"].insert('end', text)
		self.widgets["output"]["text"].see('end')
		self.widgets["output"]["text"].config(state="disabled")

	def open_file(self):
		file_names = askopenfilenames(title=self.tr("file_btn"))
		for file in file_names:
			self.widgets["file_list"].insert(END, file)
			self.widgets["file_list"].selection_set(END)

	def execute_command(self, command):
		"""
		包装命令执行流程 / Wrapped command execution flow
		
		Args:
			command (str): 操作类型 ['install'|'upgrade'|'uninstall'] / 
						  Command type ['install'|'upgrade'|'uninstall']
		
		执行流程 / Execution flow:
		1. 禁用按钮 -> 2. 执行命令 -> 3. 恢复按钮 / 
		1. Disable buttons -> 2. Execute command -> 3. Restore buttons
		"""

		self.disable_buttons()
		self.widgets["buttons"][command].config(text=f"{self.tr('executing_text')}")

		package = self.widgets["entry"].get()
		files = [self.widgets["file_list"].get(i)
				 for i in self.widgets["file_list"].curselection()]

		if files or package:
			self.show("\n\n")
		try:
			if package:
				self.package_manager.execute(command=command, name=package,
					source_url=self.sources[self.widgets["source_combobox"].get()]
						if command in ["install", "upgrade"] else None)
			if files:
				for file in files:
					self.package_manager.execute(command=command, name=file, require=True,
						source_url=self.sources[self.widgets["source_combobox"].get()]
							if command in ["install", "upgrade"] else None)
		except Exception as e:
			self.main_window.after(0, lambda: showerror("Error", str(e)))
		finally:
			self.main_window.after(0, lambda:
				self.widgets["buttons"][command].config(text=self.tr(command + '_btn')))
			self.main_window.after(0, self.enable_buttons)

	def disable_buttons(self):
		for button in self.widgets["buttons"].values():
			button.config(state="disabled")

	def enable_buttons(self):
		for button in self.widgets["buttons"].values():
			button.config(state="normal")

	def show_about_window(self):
		about_window = Toplevel(self.main_window)
		about_window.grab_set()
		about_window.focus_set()
		about_window.title(self.tr('about_title'))
		about_window.resizable(False, False)

		Label(about_window, text="-Un-Installer",
			  font=("Consolas", 20)).pack(padx=5, pady=5)
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

		Label(settings_window, text=self.tr('language_label')).grid(
			row=0, column=0, padx=5, pady=5)
		language_combobox = Combobox(settings_window, width=20, state='readonly')
		language_combobox.grid(row=0, column=1, padx=5, pady=5)
		language_combobox['values'] = tuple(self.languages.keys())
		language_combobox.set(self.settings['language'])

		Label(settings_window, text=self.tr('default_source_label')).grid(
			row=1, column=0, padx=5, pady=5)
		source_combobox = Combobox(settings_window, width=20, state='readonly')
		source_combobox.grid(row=1, column=1, padx=5, pady=5)
		source_combobox['values'] = tuple(self.sources.keys())
		source_combobox.set(self.settings['default_source'])

		def save_settings():
			self.settings['language'] = language_combobox.get()
			self.settings['default_source'] = source_combobox.get()
			save_data({
				'LANGUAGES': self.languages, 'SOURCES': self.sources,
				'settings': self.settings
			})
			settings_window.destroy()
			showinfo(self.tr('settings_btn'), self.tr('restart_prompt'))

		Button(settings_window, text=self.tr('save_btn'),
			   command=save_settings, width=20).grid(row=2, column=0, padx=5, pady=5)
		Button(settings_window, text=self.tr('cancel_btn'),
			   command=settings_window.destroy, width=20).grid(
			row=2, column=1, padx=5, pady=5)
