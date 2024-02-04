import Income_Information as Income_Info
import tkinter as tk
from tkinter import filedialog


class File_Explorer_Frame(tk.Frame):
    def __init__(self, tool_data, **kwargs):
        if tool_data is None:
            raise ValueError("file_data must be provided")

        super().__init__(**kwargs)

        self.tool_data = tool_data

        self.columnconfigure(0, weight=1, minsize=450)
        self.columnconfigure(1, weight=0, minsize=40)
        self.rowconfigure(0, weight=1, minsize=35)

        self.file_browse_btn = tk.Button(
            self,
            text="Browse Files",
            font=("Arial", 12),
            borderwidth=5,
            command=self.Browse_Files,
        )
        self.file_browse_btn.grid(row=0, column=1, sticky="NSEW")

        self.file_selected_lbl = tk.Label(
            self,
            text="Select Income File",
            font=("Arial", 12),
            relief=tk.GROOVE,
            borderwidth=5,
        )
        self.file_selected_lbl.grid(row=0, column=0, sticky="NSEW")

    def Browse_Files(self):
        file_selected = filedialog.askopenfilename(
            initialdir="c:/",
            title="Select a File",
            filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")),
        )

        if len(file_selected) > 0:
            self.file_selected_lbl.configure(text=file_selected.split("/")[-1])
            self.tool_data["file_data"] = Income_Info.Import_Income_Data(file_selected)
            self.tool_data["yearly_income_frm_ref"].refresh()
