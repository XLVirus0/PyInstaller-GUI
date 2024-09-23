import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import shutil
from datetime import datetime
import subprocess


__author__ = "XLVirus"


class PyInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyInstaller GUI")
        self.root.geometry("400x720")  # Taller window (9:16 aspect ratio)
        self.root.configure(bg='#1c1c1c')  # Dark grey background

        self.main_file = None
        self.optional_files = []
        self.icon_file = None  # Variable to store icon file path

        # Main file and optional files selection
        self.files_frame = tk.Frame(root, bg='#1c1c1c')
        self.files_frame.grid(row=0, padx=10, pady=(20, 5), sticky='ew')

        self.main_file_label = tk.Label(self.files_frame, text="Main File*", bg='#1c1c1c', fg='white', anchor='w', font=("Arial Black", 12))
        self.main_file_label.grid(row=0, column=0, padx=10, sticky='w')

        self.optional_files_label = tk.Label(self.files_frame, text="Optional Files", bg='#1c1c1c', fg='white', anchor='w', font=("Arial Black", 12))
        self.optional_files_label.grid(row=0, column=1, padx=10, sticky='w')

        self.main_file_button = tk.Button(self.files_frame, text="Browse", command=self.select_main_file, bg='#0078d4', fg='white', borderwidth=0, relief='flat', font=("Arial Black", 10), width=15)
        self.main_file_button.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='w')

        self.optional_file_button = tk.Button(self.files_frame, text="Browse", command=self.select_optional_files, bg='#0078d4', fg='white', borderwidth=0, relief='flat', font=("Arial Black", 10), width=15)
        self.optional_file_button.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='w')

        # Features Categories
        self.features_label = tk.Label(root, text="PyInstaller Options", bg='#1c1c1c', fg='white', anchor='center', font=("Arial Black", 12))
        self.features_label.grid(row=1, padx=10, pady=(10, 5), sticky='ew')

        # Checkboxes for common options
        self.console_var = tk.BooleanVar()
        self.one_file_var = tk.BooleanVar()
        self.no_window_var = tk.BooleanVar()
        self.additional_files_var = tk.BooleanVar()

        # Arrange checkboxes two by two
        self.checkbox_frame = tk.Frame(root, bg='#1c1c1c')
        self.checkbox_frame.grid(row=2, padx=10, pady=(0, 20), sticky='ew')

        tk.Checkbutton(self.checkbox_frame, text="Console", variable=self.console_var, bg='#1c1c1c', fg='white', selectcolor='#0078d4', anchor='w', font=("Arial Black", 10)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Checkbutton(self.checkbox_frame, text="One File", variable=self.one_file_var, bg='#1c1c1c', fg='white', selectcolor='#0078d4', anchor='w', font=("Arial Black", 10)).grid(row=0, column=1, padx=10, pady=5, sticky='w')
        tk.Checkbutton(self.checkbox_frame, text="GUI", variable=self.no_window_var, bg='#1c1c1c', fg='white', selectcolor='#0078d4', anchor='w', font=("Arial Black", 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Checkbutton(self.checkbox_frame, text="Additional Files", variable=self.additional_files_var, bg='#1c1c1c', fg='white', selectcolor='#0078d4', anchor='w', font=("Arial Black", 10)).grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Icon selection
        self.icon_label = tk.Label(root, text="Icon*", bg='#1c1c1c', fg='white', anchor='center', font=("Arial Black", 12))
        self.icon_label.grid(row=3, padx=10, pady=(20, 5), sticky='ew')

        self.icon_button = tk.Button(root, text="Browse for Icon", command=self.select_icon_file, bg='#0078d4', fg='white', borderwidth=0, relief='flat', font=("Arial Black", 10), width=20)
        self.icon_button.grid(row=4, padx=10, pady=(0, 20), sticky='ew')

        # Submit button
        self.submit_button = tk.Button(root, text="Build", command=self.build, bg='#0078d4', fg='white', borderwidth=0, relief='flat', font=("Arial Black", 12), width=25)
        self.submit_button.grid(row=5, padx=10, pady=30, sticky='ew')

        # Log panel
        self.log_panel = scrolledtext.ScrolledText(root, bg='#1c1c1c', fg='white', font=("Arial Black", 10), wrap='word', height=10)
        self.log_panel.grid(row=6, padx=10, pady=(10, 20), sticky='ew')

        # Make columns expand
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Resources directory
        self.resources_dir = os.path.join(os.getcwd(), "resources")
        os.makedirs(self.resources_dir, exist_ok=True)

    def select_main_file(self):
        self.main_file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.main_file:
            messagebox.showinfo("Selected File", f"Main File: {self.main_file}")

    def select_optional_files(self):
        files = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        self.optional_files = list(files)
        if self.optional_files:
            messagebox.showinfo("Selected Files", f"Optional Files: {', '.join(self.optional_files)}")

    def select_icon_file(self):
        self.icon_file = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])  # Store icon file path
        if self.icon_file:
            messagebox.showinfo("Selected Icon", f"Icon File: {self.icon_file}")

    def build(self):
        if not self.main_file:
            messagebox.showerror("Error", "Please select a main Python file.")
            return

        # Create a folder with the current date and time for each build session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        build_dir = os.path.join(self.resources_dir, timestamp)
        os.makedirs(build_dir, exist_ok=True)

        # Copy selected files to the new build directory
        shutil.copy(self.main_file, build_dir)
        for file in self.optional_files:
            shutil.copy(file, build_dir)
        if self.icon_file:
            shutil.copy(self.icon_file, build_dir)

        # Prepare PyInstaller command
        options = {
            "main_file": os.path.join(build_dir, os.path.basename(self.main_file)),
            "optional_files": [os.path.join(build_dir, os.path.basename(f)) for f in self.optional_files],
            "console": self.console_var.get(),
            "one_file": self.one_file_var.get(),
            "gui": self.no_window_var.get(),
            "icon": os.path.join(build_dir, os.path.basename(self.icon_file)) if self.icon_file else None,
            "include_additional_files": self.additional_files_var.get(),
        }

        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile" if options["one_file"] else "",
            "--noconsole" if options["gui"] else "--console",
            f"--icon={options['icon']}" if options['icon'] else "",
            options["main_file"]
        ]

        # Run PyInstaller
        self.log_panel.insert(tk.END, f"Running command: {' '.join(pyinstaller_cmd)}\n")
        self.log_panel.see(tk.END)

        try:
            result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
            self.log_panel.insert(tk.END, result.stdout)
            self.log_panel.insert(tk.END, result.stderr)
        except Exception as e:
            self.log_panel.insert(tk.END, f"Error running PyInstaller: {str(e)}\n")
        
        self.log_panel.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyInstallerApp(root)
    root.mainloop()
