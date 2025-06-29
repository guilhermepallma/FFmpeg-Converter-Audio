import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, ttk
import threading
import queue
from datetime import datetime
import converter
from languages import STRINGS

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AudioConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Converter")
        self.master.geometry("720x640")
        
        self.languages = STRINGS
        self.lang_var = tk.StringVar(value='pt')
        
        ffmpeg_path = resource_path("ffmpeg/ffmpeg.exe")
        ffprobe_path = resource_path("ffmpeg/ffprobe.exe")
        self.converter = converter.ConversionLogic(ffmpeg_path, ffprobe_path)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.SUPPORTED_EXTENSIONS = (".wav", ".mp3", ".flac", ".m4a", ".ogg")
        self.skipped_folders = []
        self.conversion_start_time = None

        self.create_menu()
        self.on_language_change()
        self.lang_var.trace_add("write", self.on_language_change)

    def _(self, key):
        return self.languages.get(self.lang_var.get(), {}).get(key, key)

    def on_language_change(self, *args):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.master.title(self._("window_title"))
        self.create_widgets()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self._("menu_language"), menu=language_menu)
        language_menu.add_radiobutton(label="Português", variable=self.lang_var, value='pt')
        language_menu.add_radiobutton(label="English", variable=self.lang_var, value='en')

    def center_toplevel(self, toplevel_window):
        toplevel_window.withdraw()
        toplevel_window.update_idletasks()
        
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        toplevel_width = toplevel_window.winfo_width()
        toplevel_height = toplevel_window.winfo_height()

        new_x = main_x + (main_width // 2) - (toplevel_width // 2)
        new_y = main_y + (main_height // 2) - (toplevel_height // 2)

        toplevel_window.geometry(f"+{new_x}+{new_y}")
        toplevel_window.deiconify()

    def format_time(self, seconds):
        if seconds < 0: seconds = 0
        seconds = int(seconds)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def show_stream_copy_help(self):
        title = self._("stream_copy_help_title")
        message = self._("stream_copy_help_msg")
        messagebox.showinfo(title, message, parent=self.master)

    def start_conversion_thread(self):
        if not self.file_listbox.get(0, tk.END):
            messagebox.showerror(self._("error_title"), self._("no_files_selected_msg"))
            return
        if not self.output_dir_path.get():
            messagebox.showerror(self._("dest_required_title"), self._("dest_required_msg"))
            return
        selected_format = self.format_var.get()
        if self.stream_copy_var.get() and selected_format in ['MP3', 'AAC']:
            messagebox.showerror(self._("invalid_op_title"), self._("invalid_op_msg").format(format=selected_format))
            return

        self.toggle_main_widgets_state(tk.DISABLED)
        progress_window = tk.Toplevel(self.master)
        progress_window.title(self._("progress_window_title"))
        progress_window.geometry("500x170")
        progress_window.resizable(False, False)
        progress_window.transient(self.master)
        progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

        status_label = tk.Label(progress_window, text=self._("status_starting"), anchor='w')
        status_label.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(progress_window, text=self._("progress_status_lbl"), anchor='w').pack(fill=tk.X, padx=15, pady=(10,0))
        total_progress = ttk.Progressbar(progress_window, orient='horizontal', length=100, mode='determinate')
        total_progress.pack(fill=tk.X, padx=15, pady=2)
        
        etr_frame = tk.Frame(progress_window)
        etr_frame.pack(fill=tk.X, padx=15, pady=5)
        tk.Label(etr_frame, text=self._("etr_label"), anchor='w').pack(side=tk.LEFT)
        etr_value_label = tk.Label(etr_frame, text=self._("etr_calculating"), anchor='w')
        etr_value_label.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(progress_window, text=self._("close_btn"), state=tk.DISABLED, command=progress_window.destroy)
        close_button.pack(pady=10)
        
        self.center_toplevel(progress_window)

        progress_widgets = {
            'status': status_label, 
            'total': total_progress, 
            'close_button': close_button,
            'etr_value': etr_value_label
        }
        conversion_params = {
            'input_files': self.file_listbox.get(0, tk.END), 'format': self.format_var.get(), 'output_dir': self.output_dir_path.get(),
            'folder_name': self.output_folder_name_var.get(), 'is_stream_copy': self.stream_copy_var.get(), 'bitrate': self.bitrate_var.get(),
            'samplerate': self.samplerate_var.get(), 'bitdepth': self.bitdepth_var.get()
        }
        
        self.conversion_start_time = datetime.now()
        app_queue = queue.Queue()
        thread = threading.Thread(target=self.converter.run_conversion, args=(conversion_params, app_queue), daemon=True)
        thread.start()
        self.master.after(100, self.process_queue, app_queue, progress_widgets)

    def process_queue(self, app_queue, progress_widgets):
        try:
            msg = app_queue.get_nowait()
            if msg['type'] == 'batch_start':
                progress_widgets['status'].config(text=self._("status_starting"))
            elif msg['type'] == 'total_progress':
                progress_widgets['total']['value'] = msg['value']
                progress_widgets['status'].config(text=self._("status_converting").format(current=msg['current'], total=msg['total'], filename=msg['filename']))
                
                if msg['current'] > 0:
                    elapsed_time = (datetime.now() - self.conversion_start_time).total_seconds()
                    avg_time_per_file = elapsed_time / msg['current']
                    files_remaining = msg['total'] - msg['current']
                    etr_seconds = avg_time_per_file * files_remaining
                    etr_formatted = self.format_time(etr_seconds)
                    progress_widgets['etr_value'].config(text=etr_formatted)

            elif msg['type'] == 'done':
                self.toggle_main_widgets_state(tk.NORMAL)
                progress_widgets['total']['value'] = 100
                progress_widgets['status'].config(text=self._("status_done"))
                progress_widgets['etr_value'].config(text="")
                progress_widgets['close_button'].config(state=tk.NORMAL)
                
                skipped_folder_info = ""
                if self.skipped_folders:
                    skipped_list = "\n- ".join(self.skipped_folders)
                    skipped_folder_info = self._("skipped_folders_msg").format(folders=skipped_list)

                if not msg['errors']:
                    base_msg = self._("conversion_success_msg").format(count=msg['success_count'], path=msg['path'])
                    final_message = base_msg + skipped_folder_info
                    messagebox.showinfo(self._("success_title"), final_message)
                else:
                    base_msg = self._("conversion_error_msg").format(count=msg['success_count'], errors="\n".join(map(str, msg['errors'])))
                    final_message = base_msg + skipped_folder_info
                    messagebox.showwarning(self._("warning_title"), final_message)
                
                self.skipped_folders.clear()
                return
            self.master.after(100, self.process_queue, app_queue, progress_widgets)
        except queue.Empty:
            self.master.after(100, self.process_queue, app_queue, progress_widgets)
    
    def select_files(self):
        filetypes_str = " ".join([f"*.{ext.strip('.')}" for ext in self.SUPPORTED_EXTENSIONS])
        filepaths = filedialog.askopenfilenames(title=self._("select_files_btn"), filetypes=[("Audio Files", filetypes_str)])
        if not filepaths: return

        existing_files = set(self.file_listbox.get(0, tk.END))
        for f in filepaths:
            if f not in existing_files:
                self.file_listbox.insert(tk.END, f)
        self.update_options_ui()

    def select_folder(self):
        directory = filedialog.askdirectory(title=self._("select_folder_btn"))
        if not directory: return

        found_files = self.scan_folder_for_audio(directory)
        
        if not found_files:
            if directory not in self.skipped_folders:
                self.skipped_folders.append(directory)
            messagebox.showwarning(
                self._("folder_ignored_warning_title"),
                self._("folder_ignored_warning_msg").format(folder=directory)
            )
            return

        existing_files = set(self.file_listbox.get(0, tk.END))
        added_count = 0
        for file_path in found_files:
            if file_path not in existing_files:
                self.file_listbox.insert(tk.END, file_path)
                added_count += 1
        
        if added_count > 0:
            self.update_options_ui()

    def scan_folder_for_audio(self, folder_path):
        audio_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(self.SUPPORTED_EXTENSIONS):
                    full_path = os.path.join(root, file)
                    audio_files.append(full_path.replace("/", "\\"))
        return audio_files

    def clear_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.skipped_folders.clear()

    def select_output_directory(self):
        directory = filedialog.askdirectory(title=self._("dest_required_title"))
        if directory: self.output_dir_path.set(directory)

    def toggle_main_widgets_state(self, state):
        for widget in self.widgets_to_toggle:
            try:
                widget.configure(state=state)
            except tk.TclError:
                pass

    def update_options_ui(self, *args):
        for widget in self.options_frame.winfo_children(): widget.destroy()
        
        self.bitrate_var.set("")
        self.samplerate_var.set("")
        self.bitdepth_var.set("")

        if self.format_var.get() in ['MP3', 'AAC']:
            self.stream_copy_checkbox.config(state=tk.DISABLED)
            self.stream_copy_var.set(False)
        else:
            self.stream_copy_checkbox.config(state=tk.NORMAL)
        new_state = tk.DISABLED if self.stream_copy_var.get() else tk.NORMAL
        
        options = converter.FORMAT_OPTIONS.get(self.format_var.get())
        if not options: return
        
        if 'bitrate' in options:
            display_values = [item[0] for item in options['bitrate']]
            if not self.stream_copy_var.get(): self.bitrate_var.set(display_values[0])
            tk.Label(self.options_frame, text=self._("quality_bitrate_lbl")).pack(side=tk.LEFT, padx=(0, 5))
            tk.OptionMenu(self.options_frame, self.bitrate_var, *display_values).pack(side=tk.LEFT, padx=(0, 15))
        if 'samplerate' in options:
            display_values = [item[0] for item in options['samplerate']]
            if not self.stream_copy_var.get(): self.samplerate_var.set(display_values[0])
            tk.Label(self.options_frame, text=self._("samplerate_lbl")).pack(side=tk.LEFT, padx=(0, 5))
            tk.OptionMenu(self.options_frame, self.samplerate_var, *display_values).pack(side=tk.LEFT, padx=(0, 15))
        if 'bitdepth' in options:
            display_values = [item[0] for item in options['bitdepth']]
            if not self.stream_copy_var.get(): self.bitdepth_var.set(display_values[0])
            tk.Label(self.options_frame, text=self._("bitdepth_lbl")).pack(side=tk.LEFT, padx=(0, 5))
            tk.OptionMenu(self.options_frame, self.bitdepth_var, *display_values).pack(side=tk.LEFT)
        
        for widget in self.options_frame.winfo_children(): widget.configure(state=new_state)

    def create_widgets(self):
        self.menu_bar.entryconfig(1, label=self._("menu_language"))
        self.format_var = tk.StringVar(value='MP3')
        self.format_var.trace_add("write", self.update_options_ui)
        self.stream_copy_var = tk.BooleanVar(value=False)
        self.output_dir_path = tk.StringVar()
        self.output_folder_name_var = tk.StringVar()
        self.bitrate_var = tk.StringVar()
        self.samplerate_var = tk.StringVar()
        self.bitdepth_var = tk.StringVar()

        content_frame = tk.Frame(self.main_frame, padx=15, pady=15)
        content_frame.pack(expand=True, fill=tk.BOTH)

        input_frame = tk.LabelFrame(content_frame, text=self._("section1_title"), padx=10, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        list_frame = tk.Frame(input_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        input_buttons_frame = tk.Frame(input_frame)
        input_buttons_frame.pack(fill=tk.X, pady=(5,0))
        self.select_files_button = tk.Button(input_buttons_frame, text=self._("select_files_btn"), command=self.select_files)
        self.select_files_button.pack(side=tk.LEFT)
        self.select_folder_button = tk.Button(input_buttons_frame, text=self._("select_folder_btn"), command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        self.clear_list_button = tk.Button(input_buttons_frame, text=self._("clear_list_btn"), command=self.clear_file_list)
        self.clear_list_button.pack(side=tk.LEFT, padx=5)

        options_main_frame = tk.LabelFrame(content_frame, text=self._("section2_title"), padx=10, pady=10)
        options_main_frame.pack(fill=tk.X, pady=5)
        format_menu_frame = tk.Frame(options_main_frame)
        format_menu_frame.pack(fill=tk.X, pady=5, anchor='w')
        tk.Label(format_menu_frame, text=self._("output_format_lbl")).pack(side=tk.LEFT, padx=(0, 10))
        self.format_menu = tk.OptionMenu(format_menu_frame, self.format_var, *converter.FORMAT_OPTIONS.keys())
        self.format_menu.pack(side=tk.LEFT)
        
        stream_copy_frame = tk.Frame(options_main_frame)
        stream_copy_frame.pack(anchor='w', pady=5)
        self.stream_copy_checkbox = tk.Checkbutton(stream_copy_frame, text=self._("preserve_quality_chk"), variable=self.stream_copy_var, command=self.update_options_ui)
        self.stream_copy_checkbox.pack(side=tk.LEFT)
        self.stream_copy_help_button = tk.Button(stream_copy_frame, text="?", relief=tk.FLAT,
                                                 command=self.show_stream_copy_help, font=("TkDefaultFont", 8, "bold"),
                                                 cursor="question_arrow", fg="blue")
        self.stream_copy_help_button.pack(side=tk.LEFT, padx=(0, 5))

        self.options_frame = tk.Frame(options_main_frame)
        self.options_frame.pack(fill=tk.X, pady=5, anchor='w')

        output_main_frame = tk.LabelFrame(content_frame, text=self._("section3_title"), padx=10, pady=10)
        output_main_frame.pack(fill=tk.X, pady=5)
        tk.Label(output_main_frame, text=self._("save_to_lbl")).pack(anchor='w')
        output_dir_frame = tk.Frame(output_main_frame)
        output_dir_frame.pack(fill=tk.X)
        self.output_path_entry = tk.Entry(output_dir_frame, textvariable=self.output_dir_path, state='readonly')
        self.output_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.browse_button = tk.Button(output_dir_frame, text=self._("browse_btn"), command=self.select_output_directory)
        self.browse_button.pack(side=tk.LEFT, padx=(5,0))
        tk.Label(output_main_frame, text=self._("output_folder_name_lbl")).pack(anchor='w', pady=(10,0))
        self.output_folder_entry = tk.Entry(output_main_frame, textvariable=self.output_folder_name_var)
        self.output_folder_entry.pack(fill=tk.X)

        self.convert_button = tk.Button(content_frame, text=self._("start_conversion_btn"), command=self.start_conversion_thread)
        self.convert_button.pack(pady=(15, 5), fill=tk.X, ipady=4)

        self.widgets_to_toggle = [
            self.select_files_button, self.select_folder_button, self.clear_list_button, self.file_listbox, self.format_menu,
            self.stream_copy_checkbox, self.stream_copy_help_button, self.options_frame, self.output_path_entry, self.browse_button,
            self.output_folder_entry, self.convert_button
        ]
        
        self.update_options_ui()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()