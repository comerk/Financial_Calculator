import tkinter as tk
from tkinter import ttk


class Data_Select_Frame(tk.Frame):
    def __init__(self, tool_data, **kwargs):
        super().__init__(**kwargs)

        self.tool_data = tool_data

        # Set up grid rows
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.Setup_Year_Select_Cmbbx()
        self.Setup_Quarter_Select_Cmbbx()

    # Widget Setup Methods
    def Setup_Year_Select_Cmbbx(self):
        # Set up year dropdown
        self.year_selected = tk.StringVar()
        self.year_selected.set("Select A Year To View")
        self.year_selected_previous = self.year_selected

        self.year_select_cmbbx = ttk.Combobox(
            master=self,
            textvariable=self.year_selected,
            values=[],
            justify="center",
            state="readonly",
        )
        self.year_select_cmbbx.grid(row=0, column=0, sticky="NSEW")

        # Set up binding actions for year cmbbx
        self.year_select_cmbbx.bind("<Enter>", self.Refresh)
        self.year_select_cmbbx.bind("<<ComboboxSelected>>", self.Update_Selections)

    def Setup_Quarter_Select_Cmbbx(self):
        # Set up quarter dropdown
        self.quarter_selected = tk.StringVar()
        self.quarter_selected.set("Select A Quarter To View")
        self.quarter_selected_previous = self.quarter_selected

        self.quarter_select_cmbbx = ttk.Combobox(
            master=self,
            textvariable=self.quarter_selected,
            values=[],
            justify="center",
            state="readonly",
        )
        self.quarter_select_cmbbx.grid(row=0, column=1, sticky="NSEW")

        # Set up binding actions for quarter cmbbx
        self.quarter_select_cmbbx.bind("<Enter>", self.Refresh)
        self.quarter_select_cmbbx.bind("<<ComboboxSelected>>", self.Update_Selections)

    # Updates Combo Boxes with the selected value
    def Update_Selections(self, *args):
        if self.year_select_cmbbx.get() != self.year_selected_previous:
            self.year_selected = self.year_select_cmbbx.get()
            self.year_selected_previous = self.year_selected
            self.year_select_cmbbx.set(self.year_selected)

            # Because year was changed quarter cmbbx needs to be reset
            self.quarter_selected = "Select A Quarter To View"
            self.quarter_selected_previous = self.quarter_selected
            self.quarter_select_cmbbx.set(self.quarter_selected)

        if self.quarter_select_cmbbx.get() != self.quarter_selected_previous:
            self.quarter_selected = self.quarter_select_cmbbx.get()
            self.quarter_selected_previous = self.quarter_selected
            self.quarter_select_cmbbx.set(self.quarter_selected)

        self.Update_Info_Panels()
        self.tool_data["city_tax_frm_ref"].refresh()

    def Update_Info_Panels(self):
        # Updates all information panels for the year and quarter selected
        for row in range(0, 3):
            for col in range(0, 2):
                if len(str(self.year_selected)) == 4:
                    self.year_selected = int(self.year_selected)
                    year_info = self.tool_data["file_data"][
                        self.year_selected
                    ].year_income_info

                    # Sets year info blocks to the data from the year selected
                    if col == 0:
                        year_info = list(year_info.values())
                        info = "{:,}".format(year_info[row])
                        self.tool_data["info_frm_ref"].data_sources["Blocks"][
                            row * 2
                        ].configure(text=f"${info}")

                    if len(str(self.quarter_selected)) == 2:
                        quarter_info = (
                            self.tool_data["file_data"][self.year_selected]
                            .quarters[self.quarter_selected]
                            .quarter_income_info
                        )

                        # Sets year info blocks to the data from the quarter selected
                        if col == 1:
                            quarter_info = list(quarter_info.values())
                            info = "{:,}".format(quarter_info[row])
                            self.tool_data["info_frm_ref"].data_sources["Blocks"][
                                col + (row * 2)
                            ].configure(text=f"${info}")
                    else:
                        if col == 1:
                            self.tool_data["info_frm_ref"].data_sources["Blocks"][
                                col + (row * 2)
                            ].configure(text="Data Pending...")

    # Updates Combo Boxes for dropdown selection
    def Refresh(self, *args):
        if self.tool_data["file_data"] is None:
            return

        # Sets selections for year select combobox to the available years in income data
        selectable_years = list(map(str, list(self.tool_data["file_data"])))
        self.year_select_cmbbx.config(values=selectable_years)

        # Attempts to set selections for quarter select combobox to the
        # available quarters in the year selected
        try:
            selectable_quarters = list(
                map(
                    str,
                    list(self.tool_data["file_data"][int(self.year_selected)].quarters),
                )
            )
            self.quarter_select_cmbbx.config(values=selectable_quarters)
        except:
            None
