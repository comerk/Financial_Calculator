import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import Income_Information_lib as Income_Info

income_data = {}

class App(tk.Tk):
    def __init__(self):

        #inharit Tk Class methods and variables
        super().__init__()
        self.geometry("600x300")
        self.minsize(width=600, height=400)

        #self.resizable(False, False)
        self.title("Year Income Info")

        for row in range(0, 3):
            for col in range(0, 3):
                self.rowconfigure(row, weight=1, minsize=35)
                self.columnconfigure(col, weight=1, minsize=200)

        # set up file select frame
        self.file_select_frm = File_Explorer_Frame(
            master=self
        )
        self.file_select_frm.grid(row=0, column=0, columnspan=3, sticky="EW")

        # set up data select frame
        self.data_select_frm = Data_Select_Frame(
            master=self, 
        )
        self.data_select_frm.grid(row=1, column=0, columnspan=2,sticky="EW")

        self.info_frm = Information_Frame(
            master=self
        )
        self.info_frm.grid(row=2, column=0, columnspan=2,sticky="EW")

        self.city_tax_frm = tk.Frame(master=self)
        self.city_tax_frm.grid(row=1,column=2,rowspan=2,sticky="NSEW")
        self.city_tax_frm.rowconfigure(0,weight=1,minsize=35)
        self.city_tax_frm.columnconfigure(0,weight=1,minsize=200)
        test = tk.Label(master=self.city_tax_frm,text="Hello",relief="sunken",borderwidth=20)
        test.grid(row=0, column=0,sticky="NSEW")

    

class File_Explorer_Frame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for index in range(0,1):
            self.columnconfigure(index, weight=1, minsize=35)
        self.rowconfigure(0, weight=1, minsize=35)

        self.file_browse_btn = tk.Button(
            self,
            text = "Browse Files",
            font=("Arial", 12),
            borderwidth=2,
            command = self.Browse_Files,
        )
        self.file_browse_btn.grid(row=0, column=2, sticky="NSE")

        self.file_selected_lbl = tk.Label(
            self,
            text="Select Income File",
            font=("Arial", 12),
            relief=tk.GROOVE,
        )
        self.file_selected_lbl.grid(row=0, column=0,sticky="NSEW")
    
    def Browse_Files(self):
        file_selected = tk.filedialog.askopenfilename(
            initialdir = "c:/",
            title = "Select a File",
            filetypes = (('excel files', '*.xlsx'), ('all files', '*.*'))
        )

        if len(file_selected) > 0:
            global income_data

            self.file_selected_lbl.configure(text=file_selected.split('/')[-1])
            income_data=Income_Info.Import_Income_Data(file_selected)
                    
class Data_Select_Frame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set up grid rows
        self.columnconfigure(0, weight=1, minsize=200)
        self.columnconfigure(1, weight=1, minsize=200)
        self.rowconfigure(0, weight=1, minsize=35)

        self.Setup_Year_Select_Cmbbx()
        self.Setup_Quarter_Select_Cmbbx()
#
        #self.city_tax_rate_scl = tk.Scale(
        #    master=self,
        #    from_=0,
        #    to=25,
        #    resolution=0.1,
        #    orient=tk.HORIZONTAL,
        #    label="City Tax %:",
        #    relief="raised",
        #    borderwidth=5
        #)
        #self.city_tax_rate_scl.grid(row=0,column=2,sticky="NSEW")
    
    # Widget Setup Methods
    def Setup_Year_Select_Cmbbx(self):
        
        # Set up year dropdown
        self.year_selected = tk.StringVar()
        self.year_selected.set("Select A Year To View")

        self.year_select_cmbbx = ttk.Combobox(
            master=self,
            textvariable=self.year_selected,
            values=[],
            justify="center",
            state="readonly",
            )
        self.year_select_cmbbx.grid(row=0, column=0,sticky="NSEW")

        # Set up bindings
        self.year_select_cmbbx.bind(
            "<Enter>", 
            self.Refresh
        )
        self.year_select_cmbbx.bind(
            "<<ComboboxSelected>>",
            self.Update_Selections
        )
    
    def Setup_Quarter_Select_Cmbbx(self):

        # Set up quarter dropdown
        self.quarter_selected = tk.StringVar()
        self.quarter_selected.set("Select A Quarter To View")

        self.quarter_select_cmbbx = ttk.Combobox(
            master=self,
            textvariable=self.quarter_selected,
            values=[],
            justify="center",
            state="readonly",
            )
        self.quarter_select_cmbbx.grid(row=0, column=1,sticky="NSEW")

        self.quarter_select_cmbbx.bind(
            "<Enter>",
            self.Refresh
        )
        self.quarter_select_cmbbx.bind(
            "<<ComboboxSelected>>",
            self.Update_Selections
        )

    # Binded Methods
    def Update_Selections(self, *args):
        if self.year_selected != "Select A Year To View":
            self.year_selected=self.year_select_cmbbx.get()
            self.year_select_cmbbx.set(self.year_selected)
            
        if self.quarter_selected != "Select A Quarter To View":
            self.quarter_selected=self.quarter_select_cmbbx.get()
            self.quarter_select_cmbbx.set(self.quarter_selected)

    def Refresh(self, *args):
        global income_data

        selectable_years = list(map(str,list(income_data)))
        self.year_select_cmbbx.config(values=selectable_years)

        try:
            selectable_quarters = list(map(str,list(income_data[int(self.year_selected)].quarters)))
            self.quarter_select_cmbbx.config(values=selectable_quarters)
        except:
            None

class Information_Frame(tk.Frame):
    def __init__(self, **kargs):
        super().__init__(**kargs)

        for row in range(0,3):
            self.rowconfigure(row, weight=1, minsize=110)
        
        for col in range(0,2):
            self.columnconfigure(col, weight=1, minsize=200)

        data_blocks = []
        for row in range(0,3):
            for col in range(0, 2):
                if  row == 0 or col < 2:
                    data_blocks.append(tk.Label(master=self,text="Hello",justify='center',relief="raised",borderwidth=10))
                    data_blocks[-1].grid(row=row,column=col,sticky="NSEW")

        #image = Image.open("./images/money.jpg")
        #render = ImageTk.PhotoImage(image)
        #image_lbl = tk.Label(master=self, image=render)
        #image_lbl.image = render
        #image_lbl.grid(row=1,column=2, rowspan=2)
            
            
        
