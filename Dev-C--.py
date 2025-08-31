# Name: Dev-C-- and C-- Language | Introduce: An IDE and a coding language
# Copyright (C) 2023~2025 YX-Studio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk, scrolledtext
from pygments import lex
from pygments.lexers import CLexer
from pygments.token import Token
import subprocess
import tempfile
import sys
import re
import io
import contextlib
import os
from datetime import datetime

class SimpleLangEditor:
    def __init__(self, root):
        self.root = root
        self.current_language = "en"
        self.setup_translations()
        self.root.title(self.tr("Dev-C-- v1.0.0"))
        self.root.geometry("1100x850")
        self.root.iconbitmap("icon/cmm.ico")
        
        self.init_dpi_awareness()
        
        self.current_font = ("Consolas", 12)
        self.dark_theme = False
        self.setup_themes()
        
        self.create_widgets()
        self.setup_scrollbars()
        self.setup_menu()
        self.bind_events()
        
        self.current_file = None
        self.update_line_numbers()
        self.update_status_bar()
        
        self.input_buffer = []
        self.waiting_for_input = False
    
    def setup_translations(self):
        self.translations = {
            "en": {
                "Advanced Code Editor": "Dev-C-- v1.0.0",
                "File": "File",
                "New": "New",
                "Open...": "Open...",
                "Save": "Save",
                "Save As...": "Save As...",
                "Clear Console": "Clear Console",
                "Exit": "Exit",
                "Edit": "Edit",
                "Undo": "Undo",
                "Redo": "Redo",
                "Cut": "Cut",
                "Copy": "Copy",
                "Paste": "Paste",
                "Find...": "Find...",
                "Font...": "Font...",
                "Toggle Theme": "Toggle Theme",
                "Language": "Language",
                "English": "English",
                "Chinese": "Chinese",
                "Run": "Run",
                "Run Script": "Run Script",
                "Stop Execution": "Stop Execution",
                "Help": "Help",
                "Syntax Help": "Syntax Help",
                "Editor Help": "Editor Help (Comming Soon)",
                "About": "About",
                "Ready": "Ready",
                "Console": "Console",
                "New file created": "New file created",
                "Console cleared": "Console cleared",
                "Execution stopped": "Execution stopped",
                "Text not found": "Text not found",
                "Found: {}": "Found: {}",
                "Error": "Error",
                "Cannot open file:\n{}": "Cannot open file:\n{}",
                "Cannot save file:\n{}": "Cannot save file:\n{}",
                "Cannot run script:\n{}": "Cannot run script:\n{}",
                "No code to run": "No code to run",
                "Script executed: {}": "Script executed: {}",
                "Theme switched to {}": "Theme switched to {}",
                "Font changed to {} {}": "Font changed to {} {}",
                "Save File": "Save File",
                "Do you want to save before running?": "Do you want to save before running?",
                "Quit": "Quit",
                "Do you want to quit?": "Do you want to quit?",
                "Unsaved Changes": "Unsaved Changes",
                "You have unsaved changes. Do you want to quit anyway?": "You have unsaved changes. Do you want to quit anyway?",
                "Select Font": "Select Font",
                "Font Family:": "Font Family:",
                "Size:": "Size:",
                "Apply": "Apply",
                "Find": "Find",
                "Close": "Close",
                "Line: {}, Col: {}": "Line: {}, Col: {}",
                "Language: {}": "Language: {}",
                "Dark": "Dark",
                "Light": "Light"
            },
            "zh": {
                "Advanced Code Editor": "Dev-C-- v1.0.0",
                "File": "文件",
                "New": "新建",
                "Open...": "打开...",
                "Save": "保存",
                "Save As...": "另存为...",
                "Clear Console": "清空控制台",
                "Exit": "退出",
                "Edit": "编辑",
                "Undo": "撤销",
                "Redo": "重做",
                "Cut": "剪切",
                "Copy": "复制",
                "Paste": "粘贴",
                "Find...": "查找...",
                "Font...": "字体...",
                "Toggle Theme": "切换主题",
                "Language": "语言",
                "English": "英文",
                "Chinese": "中文",
                "Run": "运行",
                "Run Script": "运行脚本",
                "Stop Execution": "停止执行",
                "Help": "帮助",
                "Syntax Help": "语法帮助",
                "Editor Help": "编辑器帮助 (敬请期待)",
                "About": "关于",
                "Ready": "就绪",
                "Console": "控制台",
                "New file created": "已创建新文件",
                "Console cleared": "控制台已清空",
                "Execution stopped": "执行已停止",
                "Text not found": "未找到文本",
                "Found: {}": "已找到: {}",
                "Error": "错误",
                "Cannot open file:\n{}": "无法打开文件:\n{}",
                "Cannot save file:\n{}": "无法保存文件:\n{}",
                "Cannot run script:\n{}": "无法运行脚本:\n{}",
                "No code to run": "没有可运行的代码",
                "Script executed: {}": "脚本已执行: {}",
                "Theme switched to {}": "主题已切换为 {}",
                "Font changed to {} {}": "字体已更改为 {} {}",
                "Save File": "保存文件",
                "Do you want to save before running?": "运行前是否保存?",
                "Quit": "退出",
                "Do you want to quit?": "是否退出?",
                "Unsaved Changes": "未保存的更改",
                "You have unsaved changes. Do you want to quit anyway?": "您有未保存的更改。确定要退出吗?",
                "Select Font": "选择字体",
                "Font Family:": "字体:",
                "Size:": "大小:",
                "Apply": "应用",
                "Find": "查找",
                "Close": "关闭",
                "Line: {}, Col: {}": "行: {}, 列: {}",
                "Language: {}": "语言: {}",
                "Dark": "深色",
                "Light": "浅色"
            }
        }
    
    def tr(self, text, *args):
        translation = self.translations[self.current_language].get(text, text)
        return translation.format(*args) if args else translation
    
    def setup_scrollbars(self):
        self.v_scroll = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.on_scroll
        )
        self.v_scroll.pack(side="right", fill="y")
        
        self.text.config(yscrollcommand=self.update_scroll)
        self.line_numbers.config(yscrollcommand=self.update_scroll)

    def init_dpi_awareness(self):
        if sys.platform == "win32":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
    
    def setup_themes(self):
        self.themes = {
            "light": {
                "bg": "white", "fg": "black", "cursor": "black",
                "line_bg": "#f0f0f0", "line_fg": "#666",
                "keywords": "blue", "comments": "green",
                "strings": "purple", "numbers": "red",
                "builtins": "orange",
                "select_bg": "#add8e6", "select_fg": "black",
                "console_bg": "white", "console_fg": "black",
                "console_input": "blue",
                "status_bg": "#f0f0f0", "status_fg": "#666",
                "button_bg": "#f0f0f0", "button_fg": "black"
            },
            "dark": {
                "bg": "#1e1e1e", "fg": "#d4d4d4", "cursor": "#d4d4d4",
                "line_bg": "#252526", "line_fg": "#858585",
                "keywords": "#569cd6", "comments": "#6a9955",
                "strings": "#ce9178", "numbers": "#b5cea8",
                "builtins": "#d7ba7d",
                "select_bg": "#264f78", "select_fg": "white",
                "console_bg": "#1e1e1e", "console_fg": "#d4d4d4",
                "console_input": "#569cd6",
                "status_bg": "#252526", "status_fg": "#858585",
                "button_bg": "#2d2d2d", "button_fg": "#d4d4d4"
            }
        }
    
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        self.line_numbers = tk.Text(
            self.main_frame, width=4, padx=5, pady=5,
            bg=self.themes["light"]["line_bg"], fg=self.themes["light"]["line_fg"],
            font=self.current_font, state="disabled", wrap="none",
            takefocus=0, bd=0, highlightthickness=0,
            spacing1=0, spacing2=0, spacing3=0
        )
        self.line_numbers.pack(side="left", fill="y")
        
        self.text = tk.Text(
            self.main_frame, wrap="none", font=self.current_font,
            bg=self.themes["light"]["bg"], fg=self.themes["light"]["fg"],
            insertbackground=self.themes["light"]["cursor"],
            selectbackground=self.themes["light"]["select_bg"],
            selectforeground=self.themes["light"]["select_fg"],
            padx=5, pady=5, undo=True,
            spacing1=0, spacing2=0, spacing3=0,
            bd=0, highlightthickness=0
        )
        self.text.pack(side="left", fill="both", expand=True)
        
        self.console_frame = tk.Frame(self.root)
        self.console_frame.pack(fill="both", expand=False)
        
        self.console_label = tk.Label(
            self.console_frame, text=self.tr("Console"), 
            bg=self.themes["light"]["line_bg"], fg=self.themes["light"]["line_fg"],
            anchor="w", padx=5
        )
        self.console_label.pack(fill="x")
        
        self.console_output = scrolledtext.ScrolledText(
            self.console_frame, wrap="word", 
            bg=self.themes["light"]["console_bg"], fg=self.themes["light"]["console_fg"],
            font=self.current_font, state="disabled",
            height=10, padx=5, pady=5
        )
        self.console_output.pack(fill="both", expand=True)
        
        self.console_input_frame = tk.Frame(self.console_frame)
        self.console_input_frame.pack(fill="x", padx=5, pady=(0,5))
        
        tk.Label(self.console_input_frame, text=">").pack(side="left")
        self.console_input = ttk.Entry(
            self.console_input_frame, 
            font=self.current_font
        )
        self.console_input.pack(side="left", fill="x", expand=True)
        self.console_input.bind("<Return>", self.handle_console_input)
        
        self.status_bar = tk.Frame(
            self.root, bd=1, relief="sunken",
            bg=self.themes["light"]["status_bg"]
        )
        self.status_bar.pack(fill="x")
        
        self.status_label = tk.Label(
            self.status_bar, text=self.tr("Ready"), 
            bg=self.themes["light"]["status_bg"], fg=self.themes["light"]["status_fg"],
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True, padx=5)
        
        self.language_label = tk.Label(
            self.status_bar, text=self.tr("Language: {}").format(self.current_language.upper()), 
            bg=self.themes["light"]["status_bg"], fg=self.themes["light"]["status_fg"],
            anchor="e"
        )
        self.language_label.pack(side="right", padx=5)
        
        self.line_col_label = tk.Label(
            self.status_bar, text=self.tr("Line: {}, Col: {}").format(1, 1), 
            bg=self.themes["light"]["status_bg"], fg=self.themes["light"]["status_fg"],
            anchor="e"
        )
        self.line_col_label.pack(side="right", padx=5)
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self.tr("New"), accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label=self.tr("Open..."), accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label=self.tr("Save"), accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label=self.tr("Save As..."), command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label=self.tr("Clear Console"), command=self.clear_console)
        file_menu.add_separator()
        file_menu.add_command(label=self.tr("Exit"), command=self.quit_editor)
        menubar.add_cascade(label=self.tr("File"), menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label=self.tr("Undo"), accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label=self.tr("Redo"), accelerator="Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label=self.tr("Cut"), accelerator="Ctrl+X", command=self.cut)
        edit_menu.add_command(label=self.tr("Copy"), accelerator="Ctrl+C", command=self.copy)
        edit_menu.add_command(label=self.tr("Paste"), accelerator="Ctrl+V", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label=self.tr("Find..."), accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_separator()
        edit_menu.add_command(label=self.tr("Font..."), command=self.change_font)
        edit_menu.add_command(label=self.tr("Toggle Theme"), command=self.toggle_theme)
        
        lang_menu = tk.Menu(edit_menu, tearoff=0)
        lang_menu.add_command(label=self.tr("English"), command=lambda: self.change_language("en"))
        lang_menu.add_command(label=self.tr("Chinese"), command=lambda: self.change_language("zh"))
        edit_menu.add_cascade(label=self.tr("Language"), menu=lang_menu)
        
        menubar.add_cascade(label=self.tr("Edit"), menu=edit_menu)
        
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label=self.tr("Run Script"), accelerator="F5", command=self.run_script)
        run_menu.add_command(label=self.tr("Stop Execution"), accelerator="F6", command=self.stop_execution)
        menubar.add_cascade(label=self.tr("Run"), menu=run_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self.tr("Syntax Help"), command=self.show_syntax_help)
        help_menu.add_command(label=self.tr("Editor Help (Comming Soon)"))#, command=self.show_editor_help)
        help_menu.add_separator()
        help_menu.add_command(label=self.tr("About"), command=self.show_about)
        menubar.add_cascade(label=self.tr("Help"), menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def change_language(self, language):
        if language in self.translations:
            self.current_language = language
            self.update_ui_language()
            self.status(self.tr("Language changed to {}").format(language.upper()))
    
    def update_ui_language(self):
        self.root.title(self.tr("Dev-C-- v1.0.0"))
        
        self.setup_menu()
        
        self.console_label.config(text=self.tr("Console"))
        
        self.status_label.config(text=self.tr("Ready"))
        self.update_status_bar()
    
    def clear_console(self):
        self.console_output.config(state="normal")
        self.console_output.delete("1.0", "end")
        self.console_output.config(state="disabled")
        self.status(self.tr("Console cleared"))
    
    def handle_console_input(self, event=None):
        if not self.waiting_for_input:
            return
        
        input_text = self.console_input.get()
        self.console_input.delete(0, "end")
        
        self.input_buffer.append(input_text)
        
        self.write_to_console(f"> {input_text}\n", is_input=True)
        
        self.waiting_for_input = False
    
    def write_to_console(self, text, is_input=False):
        theme = self.themes["dark"] if self.dark_theme else self.themes["light"]
        self.console_output.config(state="normal")
        
        if is_input:
            self.console_output.insert("end", text, "input")
            self.console_output.tag_config("input", foreground=theme["console_input"])
        else:
            self.console_output.insert("end", text)
        
        self.console_output.see("end")
        self.console_output.config(state="disabled")
    
    def custom_input(self, prompt=""):
        if prompt:
            self.write_to_console(prompt)
        
        self.waiting_for_input = True
        
        self.console_input.focus()
        
        while self.waiting_for_input:
            self.root.update()
        
        return self.input_buffer.pop(0)
    
    def bind_events(self):
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<<Modified>>", self.on_text_modified)
        self.text.bind("<Key>", self.update_status_bar)
        self.text.bind("<Button-1>", self.update_status_bar)
        
        self.text.bind("<Return>", self.auto_indent)
        
        self.text.bind("<MouseWheel>", self.on_scroll)
        if sys.platform.startswith("linux"):
            self.text.bind("<Button-4>", lambda e: self.on_scroll(-1))
            self.text.bind("<Button-5>", lambda e: self.on_scroll(1))
        
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
        self.root.bind_all("<F5>", lambda e: self.run_script())
        self.root.bind_all("<F6>", lambda e: self.stop_execution())
        self.root.bind_all("<Control-f>", lambda e: self.find_text())
        self.root.bind_all("<Control-z>", lambda e: self.undo())
        self.root.bind_all("<Control-y>", lambda e: self.redo())
    
    def auto_indent(self, event=None):
        current_line = self.text.get("insert linestart", "insert")
        leading_spaces = len(current_line) - len(current_line.lstrip())
        
        if current_line.rstrip().endswith('{'):
            leading_spaces += 4
        
        self.text.insert("insert", "\n" + " " * leading_spaces)
        return "break"
    
    def update_line_numbers(self, event=None):
        text_content = self.text.get("1.0", "end-1c")
        lines = text_content.split("\n")
        line_count = len(lines)
        
        max_line_num_width = len(str(max(1, line_count))) + 1
        self.line_numbers.config(width=max(max_line_num_width, 4))
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        
        first_visible_line = int(self.text.index("@0,0").split(".")[0])
        dlineinfo = self.text.dlineinfo("@0,0")
        
        if dlineinfo and line_count > 100:
            line_height = dlineinfo[3]
            visible_lines = int(self.text.winfo_height() / line_height) + 2
            last_line = min(first_visible_line + visible_lines, line_count)
            for i in range(first_visible_line, last_line + 1):
                self.line_numbers.insert("end", f"{i}\n")
        else:
            for i in range(1, line_count + 1):
                self.line_numbers.insert("end", f"{i}\n")
        
        self.line_numbers.config(state="disabled")
        
        self.line_numbers.yview_moveto(self.text.yview()[0])
        self.line_numbers.update_idletasks()
    
    def on_text_modified(self, event=None):
        if self.text.edit_modified():
            self.update_line_numbers()
            self.highlight_syntax()
            self.update_status_bar()
            self.text.edit_modified(False)
    
    def on_key_release(self, event=None):
        self.on_text_modified()
    
    def update_scroll(self, *args):
        self.text.yview_moveto(args[0])
        self.line_numbers.yview_moveto(args[0])
        self.v_scroll.set(*args)
    
    def on_scroll(self, *args):
        if len(args) == 1 and isinstance(args[0], tk.Event):
            event = args[0]
            if hasattr(event, 'delta'):
                delta = -1 if event.delta > 0 else 1
                self.text.yview("scroll", delta, "units")
        elif len(args) == 1 and isinstance(args[0], int):
            self.text.yview("scroll", args[0], "units")
        else:
            self.text.yview(*args)
        
        self.update_line_numbers()
        return "break"
    
    def highlight_syntax(self):
        code = self.text.get("1.0", "end-1c")
        
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", "end")
        
        lexer = CLexer()
        tokens = lex(code, lexer)
        
        theme = self.themes["dark"] if self.dark_theme else self.themes["light"]
        
        for token_type, value in tokens:
            if token_type in Token.Keyword:
                tag_name = "keyword"
                color = theme["keywords"]
            elif token_type in Token.Comment:
                tag_name = "comment"
                color = theme["comments"]
            elif token_type in Token.String:
                tag_name = "string"
                color = theme["strings"]
            elif token_type in Token.Number:
                tag_name = "number"
                color = theme["numbers"]
            elif token_type in Token.Name.Builtin:
                tag_name = "builtin"
                color = theme["builtins"]
            else:
                continue
            
            start = "1.0"
            while True:
                start = self.text.search(re.escape(value), start, stopindex="end", regexp=True)
                if not start:
                    break
                end = f"{start}+{len(value)}c"
                self.text.tag_add(tag_name, start, end)
                self.text.tag_config(tag_name, foreground=color)
                start = end
    
    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        theme = self.themes["dark"] if self.dark_theme else self.themes["light"]
        
        self.text.config(
            bg=theme["bg"], fg=theme["fg"],
            insertbackground=theme["cursor"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"]
        )
        self.line_numbers.config(
            bg=theme["line_bg"], fg=theme["line_fg"]
        )
        self.console_output.config(
            bg=theme["console_bg"], fg=theme["console_fg"]
        )
        self.console_label.config(
            bg=theme["line_bg"], fg=theme["line_fg"]
        )
        self.status_bar.config(
            bg=theme["status_bg"]
        )
        self.status_label.config(
            bg=theme["status_bg"], fg=theme["status_fg"]
        )
        self.language_label.config(
            bg=theme["status_bg"], fg=theme["status_fg"]
        )
        self.line_col_label.config(
            bg=theme["status_bg"], fg=theme["status_fg"]
        )
        
        self.highlight_syntax()
        self.status(self.tr("Theme switched to {}").format(self.tr("Dark") if self.dark_theme else self.tr("Light")))
    
    def change_font(self):
        font_window = tk.Toplevel(self.root)
        font_window.title(self.tr("Select Font"))
        font_window.resizable(False, False)
        
        tk.Label(font_window, text=self.tr("Font Family:")).grid(row=0, column=0, padx=5, pady=5)
        font_family = tk.StringVar(value=self.current_font[0])
        family_menu = ttk.Combobox(
            font_window, textvariable=font_family, 
            values=font.families(), state="readonly", width=30
        )
        family_menu.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(font_window, text=self.tr("Size:")).grid(row=1, column=0, padx=5, pady=5)
        font_size = tk.IntVar(value=self.current_font[1])
        size_menu = ttk.Spinbox(font_window, from_=8, to=36, textvariable=font_size, width=5)
        size_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        preview_label = tk.Label(
            font_window, text="AaBbCcDdEeFfGg 1234567890",
            font=(font_family.get(), font_size.get())
        )
        preview_label.grid(row=2, columnspan=2, pady=10)
        
        def update_preview(*args):
            try:
                preview_label.config(font=(font_family.get(), font_size.get()))
            except:
                pass
        
        font_family.trace_add("write", update_preview)
        font_size.trace_add("write", update_preview)
        
        def apply_font():
            try:
                self.current_font = (font_family.get(), font_size.get())
                self.text.config(font=self.current_font)
                self.line_numbers.config(font=self.current_font)
                self.console_output.config(font=self.current_font)
                self.console_input.config(font=self.current_font)
                font_window.destroy()
                self.update_line_numbers()
                self.status(self.tr("Font changed to {} {}").format(font_family.get(), font_size.get()))
            except Exception as e:
                messagebox.showerror(self.tr("Error"), self.tr("Invalid font: {}").format(e))
        
        ttk.Button(font_window, text=self.tr("Apply"), command=apply_font).grid(row=3, columnspan=2, pady=5)
    
    def new_file(self, event=None):
        self.text.delete("1.0", "end")
        self.current_file = None
        self.update_status_bar()
        self.status(self.tr("New file created"))
    
    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("C-- Files", "*.cmm"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text.delete("1.0", "end")
                    self.text.insert("1.0", f.read())
                self.current_file = file_path
                self.status(self.tr("Opened: {}").format(file_path))
                self.highlight_syntax()
                self.update_line_numbers()
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror(self.tr("Error"), self.tr("Cannot open file:\n{}").format(e))
    
    def save_file(self, event=None):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.text.get("1.0", "end-1c"))
                self.text.edit_modified(False)
                self.update_status_bar()
                self.status(self.tr("Saved: {}").format(self.current_file))
            except Exception as e:
                messagebox.showerror(self.tr("Error"), self.tr("Cannot save file:\n{}").format(e))
        else:
            self.save_as()
    
    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".cmm",
            filetypes=[("C-- Files", "*.cmm"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.update_status_bar()
    
    def run_script(self, event=None):
        if not self.text.get("1.0", "end-1c").strip():
            self.status(self.tr("No code to run"))
            return
        
        self.input_buffer = []
        
        if not self.current_file:
            if not messagebox.askyesno(self.tr("Save File"), self.tr("Do you want to save before running?")):
                return
            self.save_as()
            if not self.current_file:
                return
        
        try:
            class ConsoleOutput(io.StringIO):
                def __init__(self, editor):
                    super().__init__()
                    self.editor = editor
                
                def write(self, text):
                    self.editor.write_to_console(text)
            
            output_redirect = ConsoleOutput(self)
            
            import builtins
            original_input = builtins.input
            builtins.input = self.custom_input
            
            code = self.text.get("1.0", "end-1c")
            
            self.write_to_console(f"=== {self.tr('Running script:')} {self.current_file} ===\n")
            self.write_to_console(f"{self.tr('Start time:')} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            with contextlib.redirect_stdout(output_redirect), \
                 contextlib.redirect_stderr(output_redirect):
                try:
                    exec(code, {'__name__': '__main__'})
                except Exception as e:
                    self.write_to_console(f"\n{self.tr('Error:')} {str(e)}\n")
            
            builtins.input = original_input
            
            self.write_to_console(f"\n=== {self.tr('Execution finished at')} {datetime.now().strftime('%H:%M:%S')} ===\n\n")
            self.status(self.tr("Script executed: {}").format(self.current_file))
            
        except Exception as e:
            messagebox.showerror(self.tr("Error"), self.tr("Cannot run script:\n{}").format(e))
    
    def stop_execution(self):
        if self.waiting_for_input:
            self.input_buffer.append("")
            self.waiting_for_input = False
            self.write_to_console(f"{self.tr('Execution stopped by user')}\n")
            self.status(self.tr("Execution stopped"))
    
    def show_syntax_help(self):
        help_text = f"""C--语法帮助
C-- Syntax Help

输入输出 | O/I
---------------
结构 Structure
- print(输出信息MESSAGE);  // 输出 | Output text to console
- 变量名NAME = input(提示信息MESSAGE);  // 输入 | Get user input from console

示例 Example
- print("你好 Hello");
- name = input("你叫什么 What's your name");


变量 | Variables
-------------------
结构 Structure
- 变量名NAME = 表达式EXPRESSION;

示例 Example
- age = 13;
- name = "ZTY";
- is_male = true;


条件语句 | Control Structures
-------------------------------
结构 Structure
- if (条件CONDITION) {{
      // 执行的代码 Codes
  }} else if (条件CONDITION) {{
      // 执行的代码 Codes
  }} else {{
      // 执行的代码 Codes
  }}

示例 Example
- if (x == 0) {{
      print("x = 0");
  }} else if ( x > 0) {{
      print("x > 0");
  }} else {{
      print("x < 0");
  }}


循环 | Loops
--------------
结构 Structure
- for (int i = 0; i < 5; i ++) {{
      // 重复执行的代码 Codes
  }}
  // 定义变量i为0,如果i<5成立那么执行{{}}内的内容,每执行一次,将i设为原来的i+1
  // 用数学符号表示即:
  //  5
  //  Σ (假设这里就是要重复执行的代码 codes)
  // i=0
- while (CONDITION) {{
      // {self.tr("code")}
  }}
  // 如果()中CONDITION成立那么执行{{}}内的内容

示例 Example
- for(int i=1;i<=10;i++){{
      print(i);
  }}
- x = true
  while(x){{
      print("xxx");
      x = false;
  }}

运算符 | Operators
--------------------
结构 Structure
- 基本运算 Arithmetic
  符号  名字  对应数学中的符号
  Sign Name    Math Sign
   +    加         +
   -    减         -
   *    乘         ×
   /    除         ÷
   %   取余       mod
   **   幂         ^
- 比较运算 Comparison
  符号   名字   对应数学中的符号
  Sign  Name     Math Sign
   ==    等于          =
   !=   不等于         ≠
   >     大于          >
   <     小于          <
   >=  大于等于         ≥
   <=  小于等于         ≤
- 逻辑运算 Logical
  符号   名字   对应数学中的符号
  Sign  Name     Math Sign
   &&    与          ∧
   ||    或          ∨
   !     非          ¬

示例 Example
- print(5 % 3);
  print(2 ** 2);
  print(2 != 4);
  print(true || false);

=================================
Copyright 2023~2025 YXStudio .
v1.0.0
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title(self.tr("Syntax Help"))
        help_window.geometry("600x500")
        help_window.iconbitmap("icon/cmm.ico")
        
        frame = tk.Frame(help_window)
        frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        text = tk.Text(
            frame, wrap="word", padx=10, pady=10,
            yscrollcommand=scrollbar.set
        )
        text.insert("1.0", help_text)
        text.config(state="disabled")
        text.pack(fill="both", expand=True)
        
        scrollbar.config(command=text.yview)
        
        close_button = ttk.Button(
            help_window, text=self.tr("Close"), command=help_window.destroy
        )
        close_button.pack(pady=5)
    
#     def show_editor_help(self):
#         help_text = f"""Dev-C-- 编辑器帮助
# Dev-C-- Editor Help
# ======================
# 文件菜单 | File Menu
# - New: Create a new file 新建文件 (Ctrl+N)
# - Open: {self.tr("Open an existing file")} (Ctrl+O)
# - Save: {self.tr("Save current file")} (Ctrl+S)
# - Save As: {self.tr("Save with a new name")}
# - {self.tr("Clear Console")}: {self.tr("Clear the output console")}
# - {self.tr("Exit")}: {self.tr("Quit the editor")}

# {self.tr("Edit Menu")}:
# - {self.tr("Undo")}: {self.tr("Undo last action")} (Ctrl+Z)
# - {self.tr("Redo")}: {self.tr("Redo undone action")} (Ctrl+Y)
# - {self.tr("Cut")}: {self.tr("Cut selected text")} (Ctrl+X)
# - {self.tr("Copy")}: {self.tr("Copy selected text")} (Ctrl+C)
# - {self.tr("Paste")}: {self.tr("Paste from clipboard")} (Ctrl+V)
# - {self.tr("Find")}: {self.tr("Search for text")} (Ctrl+F)
# - {self.tr("Font")}: {self.tr("Change editor font")}
# - {self.tr("Toggle Theme")}: {self.tr("Switch between light/dark themes")}
# - {self.tr("Language")}: {self.tr("Switch between English/Chinese interface")}

# {self.tr("Run Menu")}:
# - {self.tr("Run Script")}: {self.tr("Execute current code")} (F5)
# - {self.tr("Stop Execution")}: {self.tr("Stop running script")} (F6)

# {self.tr("Help Menu")}:
# - {self.tr("Syntax Help")}: {self.tr("Show language syntax reference")}
# - {self.tr("Editor Help")}: {self.tr("Show this help document")}
# - {self.tr("About")}: {self.tr("Show editor information")}

# {self.tr("Additional Features")}:
# - {self.tr("Syntax highlighting for better code readability")}
# - {self.tr("Line numbers for easy navigation")}
# - {self.tr("Integrated console for program output")}
# - {self.tr("Auto-indentation for clean code formatting")}
# - {self.tr("Status bar with line/column and language info")}
# """
        
#         help_window = tk.Toplevel(self.root)
#         help_window.title(self.tr("Editor Help"))
#         help_window.geometry("700x600")
        
#         frame = tk.Frame(help_window)
#         frame.pack(fill="both", expand=True)
        
#         scrollbar = ttk.Scrollbar(frame)
#         scrollbar.pack(side="right", fill="y")
        
#         text = tk.Text(
#             frame, wrap="word", padx=10, pady=10,
#             yscrollcommand=scrollbar.set
#         )
#         text.insert("1.0", help_text)
#         text.config(state="disabled")
#         text.pack(fill="both", expand=True)
        
#         scrollbar.config(command=text.yview)
        
#         close_button = ttk.Button(
#             help_window, text=self.tr("Close"), command=help_window.destroy
#         )
#         close_button.pack(pady=5)
    
    def show_about(self):
        about_text = f"""# 编辑器版本 | Editor Version: 1.0.0
# C--语言版本 | Language Vertion: 1.0.0
# 作者 | Author: YXStudio
# 日期 | Date: 2025/8/17

# 编辑器特性 | Features:
- 支持中英文 | Support for English/Chinese interface
- 支持语法高亮 | Syntax highlighting
- 明亮和黑暗主题 | Light and dark themes
- 自带帮助文档 | Help file

# 关于C-- | About C--:
- 一个自制语言,灵感源于C++
- 更简便的C
- 基于Python构建
- 解释语言

# 开源协议 AGPL-3 以下为协议摘要:
您可以传递程序的原始源代码，需保留版权声明、许可证及无担保声明，并向接收者提供本许可证副本。
基于程序的作品需以源代码形式传递，并满足以下条件：
a) 注明修改及日期；
b) 声明适用本许可证及第7条的附加条款；
c) 整体授权；
d) 交互界面需显示适当法律声明（若原程序未显示，则无需补充）。
传递目标代码时，需同时以以下方式提供对应源代码：
a) 随物理产品附源代码；
b) 提供书面报价（有效期3年）；
c) 非商业性零星传递时附带源代码报价；
d) 通过网络服务器提供等效访问。
违反本许可证将自动终止授权，但及时纠正可恢复权利。
修改版本若支持远程交互，必须向用户提供通过网络获取对应源代码的机会。
无担保：程序按“原样”提供，不承担任何质量或性能风险。
不承担赔偿责任：除非法律要求，版权持有者不对使用或无法使用程序导致的任何损害负责。
以上摘要仅为AGPL协议的部分,不具备法律效力,原协议见本文件所在目录中LICENCE.txt

# 网站 | Website: https://www.yxstudio.mysxl.cn

Copyright (C) 2023~2025 YX-Studio
"""
        
        about_window = tk.Toplevel(self.root)
        about_window.title(self.tr("About"))
        about_window.geometry("500x400")
        about_window.iconbitmap("icon/cmm.ico")
        about_window.resizable(False, False)
        
        icon_label = tk.Label(about_window, text="Dev-C-- | C-- Language", font=("Consolas", 24))
        icon_label.pack(pady=10)
        
        text = tk.Text(about_window, wrap="word", padx=10, pady=10)
        text.insert("1.0", about_text)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        close_button = ttk.Button(
            about_window, text=self.tr("Close"), command=about_window.destroy
        )
        close_button.pack(pady=5)
    
    def undo(self):
        try:
            self.text.edit_undo()
            self.update_status_bar()
        except:
            pass
    
    def redo(self):
        try:
            self.text.edit_redo()
            self.update_status_bar()
        except:
            pass
    
    def cut(self):
        self.text.event_generate("<<Cut>>")
    
    def copy(self):
        self.text.event_generate("<<Copy>>")
    
    def paste(self):
        self.text.event_generate("<<Paste>>")
    
    def find_text(self):
        find_window = tk.Toplevel(self.root)
        find_window.title(self.tr("Find"))
        find_window.transient(self.root)
        find_window.resizable(False, False)
        
        tk.Label(find_window, text=self.tr("Find:")).grid(row=0, column=0, padx=5, pady=5)
        find_entry = ttk.Entry(find_window, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        find_entry.focus()
        
        def do_find():
            text_to_find = find_entry.get()
            if text_to_find:
                start_pos = self.text.search(
                    text_to_find, "1.0", 
                    stopindex="end", nocase=True
                )
                if start_pos:
                    end_pos = f"{start_pos}+{len(text_to_find)}c"
                    self.text.tag_remove("found", "1.0", "end")
                    self.text.tag_add("found", start_pos, end_pos)
                    self.text.tag_config("found", background="yellow")
                    self.text.see(start_pos)
                    self.status(self.tr("Found: {}").format(text_to_find))
                else:
                    self.status(self.tr("Text not found"))
        
        ttk.Button(find_window, text=self.tr("Find"), command=do_find).grid(row=1, columnspan=2, pady=5)
    
    def status(self, message):
        self.status_label.config(text=message)
    
    def update_status_bar(self, event=None):
        cursor_pos = self.text.index(tk.INSERT)
        line, col = cursor_pos.split(".")
        self.line_col_label.config(text=self.tr("Line: {}, Col: {}").format(line, col))
        
        self.language_label.config(text=self.tr("Language: {}").format(self.current_language.upper()))
        
        if self.text.edit_modified():
            modified = "*" if self.current_file else f"{self.tr('New File')} *"
            filename = os.path.basename(self.current_file) if self.current_file else self.tr("Untitled")
            self.root.title(f"{self.tr('Advanced Code Editor')} - {filename}{modified}")
        else:
            filename = os.path.basename(self.current_file) if self.current_file else self.tr("Untitled")
            self.root.title(f"{self.tr('Advanced Code Editor')} - {filename}")
    
    def quit_editor(self):
        if self.text.edit_modified():
            if not messagebox.askyesno(
                self.tr("Unsaved Changes"), 
                self.tr("You have unsaved changes. Do you want to quit anyway?")
            ):
                return
        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleLangEditor(root)
    root.mainloop()