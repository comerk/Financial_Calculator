import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter


class Yearly_Income_Frame(tk.Frame):
    def __init__(self, tool_data, **kwargs):
        super().__init__(**kwargs)

        self.tool_data = tool_data

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(2, 1))
        self.ax = self.fig.add_subplot(111)

    def refresh(self):
        years = list(map(str, list(self.tool_data["file_data"])))[::-1]
        gross_values = []
        net_values = []
        for year in years:
            gross_values.append(
                self.tool_data["file_data"][int(year)].year_income_info["Gross Income"]
            )
            net_values.append(
                self.tool_data["file_data"][int(year)].year_income_info["Net Income"]
            )

        self.ax.bar(years, gross_values, width=0.4, label="Gross", align="edge")
        self.ax.bar(years, net_values, width=0.4, label="Net", align="center")

        def format(y, pos):
            return f"${y/1000:.0f}K"

        self.ax.yaxis.set_major_formatter(FuncFormatter(format))
        self.ax.tick_params(axis="both", which="major", labelsize=10)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, padx=10, sticky="NSEW")
