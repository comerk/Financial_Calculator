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
        self.geometry("600x400")
        self.resizable(0,0)

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

        # set up information frame
        self.info_frm = Information_Frame(
            master=self
        )
        self.info_frm.grid(row=2, column=0, columnspan=2,sticky="EW")
        self.data_select_frm.info_frm = self.info_frm

        # set up city tax frame
        self.city_tax_frm = City_Tax_Frame(master=self)
        self.city_tax_frm.grid(row=1,column=2,rowspan=2,sticky="NSEW")

class File_Explorer_Frame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.columnconfigure(0, weight=2, minsize=450)
        self.columnconfigure(1, weight=1, minsize=45)
        self.rowconfigure(0, weight=1, minsize=35)

        self.file_browse_btn = tk.Button(
            self,
            text = "Browse Files",
            font=("Arial", 12),
            borderwidth=5,
            command = self.Browse_Files,
        )
        self.file_browse_btn.grid(row=0, column=1, sticky="NSEW")

        self.file_selected_lbl = tk.Label(
            self,
            text="Select Income File",
            font=("Arial", 12),
            relief=tk.GROOVE,
            borderwidth=5
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
        for col in range(0,2):
            self.columnconfigure(col, weight=1, minsize=200)
        self.rowconfigure(0, weight=1, minsize=35)

        self.Setup_Year_Select_Cmbbx()
        self.Setup_Quarter_Select_Cmbbx()
    
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

    # Updates Combo Boxes with the selected value
    def Update_Selections(self, *args):
        if self.year_select_cmbbx.get() != "Select A Year To View":
            self.year_selected=self.year_select_cmbbx.get()
            self.year_select_cmbbx.set(self.year_selected)
            
        if self.quarter_select_cmbbx.get() != "Select A Quarter To View":
            self.quarter_selected=self.quarter_select_cmbbx.get()
            self.quarter_select_cmbbx.set(self.quarter_selected)

        self.year_selected = self.year_selected
        self.quarter_selected = self.quarter_selected
        
        for row in range(0,3):
            for col in range(0,2):
                if len(str(self.year_selected)) == 4:
                    self.year_selected = int(self.year_selected)
                    year_info = income_data[self.year_selected].year_income_info
                    if col == 0:
                        year_info = list(year_info.values())
                        info = '{:,}'.format(year_info[row])
                        self.info_frm.data_sources["Blocks"][row*2].configure(text=f"${info}")

                    if len(str(self.quarter_selected)) == 2:
                        quarter_info = income_data[self.year_selected].quarters[self.quarter_selected].quarter_income_info
                        if col == 1:
                            quarter_info = list(quarter_info.values())
                            info = '{:,}'.format(quarter_info[row])
                            self.info_frm.data_sources["Blocks"][col+(row*2)].configure(text=f"${info}")

    # Updates Combo Boxes for dropdown selection
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

        data_labels = (
            ["Year Gross Income","Year Net Income","Year Taxed Amount"],
            ["Quarter Gross Income","Quarter Net Income","Quarter Taxed Amount"]
            )
        
        self.data_sources = {"Frames": [], "Blocks":[]}

        for row in range(0,3):
            #Information Frame Grid Setup -> Row
            self.rowconfigure(row, weight=1, minsize=110)
            for col in range(0, 2):
                #Information Frame Grid Setup -> Col
                self.columnconfigure(col, weight=1, minsize=200)

                #Create Frame for one of Information Frame's Grid sectors
                self.data_sources["Frames"].append(tk.Frame(master=self))

                #Setup New Frame's own grid
                self.data_sources["Frames"][-1].rowconfigure(0,weight=1, minsize=25)
                self.data_sources["Frames"][-1].rowconfigure(1,weight=1, minsize=75)
                self.data_sources["Frames"][-1].columnconfigure(0,weight=1, minsize=200)

                #Create header label for the internal frame
                header_lbl=tk.Label(
                        master=self.data_sources["Frames"][-1],
                        text=data_labels[col][row],
                        justify='center',
                        relief="raised",
                        borderwidth=5,
                        font=("Arial", 12),
                    )

                #Create data block label for the internal frame
                self.data_sources["Blocks"].append(
                    tk.Label(
                        master=self.data_sources["Frames"][-1],
                        text="Data Pending...",
                        justify='center',
                        relief="raised",
                        font=("Arial", 16),
                    )
                )
                
                #Place header inside internal frame at (0,0)
                header_lbl.grid(row=0,column=0,sticky="EW")
                #Place data block inside internal frame at (1,0)
                self.data_sources["Blocks"][-1].grid(row=1,column=0,sticky="NSEW")

                #Assign internal frame to Information Frame's grid at (row,col)
                self.data_sources["Frames"][-1].grid(row=row,column=col,sticky="NSEW")
       
class City_Tax_Frame(tk.Frame):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        
        self.rowconfigure(0, weight=1,minsize=75)
        self.rowconfigure(1, weight=1,minsize=70)
        self.rowconfigure(2, weight=1,minsize=100)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0,weight=1,minsize=200)
            
        self.sub_frm = tk.Frame(
            master=self,
            relief="raised",
            borderwidth=5
        )
        self.sub_frm.grid(row=0,column=0,rowspan=2,sticky="NSEW")
        
        self.sub_frm.rowconfigure(0, weight=1,minsize=75)
        self.sub_frm.rowconfigure(1, weight=1,minsize=60)
        self.sub_frm.columnconfigure(0,weight=1,minsize=190)

        self.city_tax_rate_scl = tk.Scale(
            master=self.sub_frm,
            from_=0,
            to=25,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="City Tax %:",
            borderwidth=2
        )
        self.city_tax_rate_scl.grid(row=0,column=0,sticky="NSEW")

        self.city_tax_lbl = tk.Label(
            master=self.sub_frm,
            text="Hello",
            relief="ridge"
        )
        self.city_tax_lbl.grid(row=1, column=0,sticky="NSEW")

        image = Image.open("./images/money.jpg")
        render = ImageTk.PhotoImage(image)
        image_lbl = tk.Label(master=self, image=render)
        image_lbl.image = render    
        image_lbl.grid(row=2,column=0, rowspan=2)