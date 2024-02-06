import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import numpy as np


class Yearly_Income_Frame(tk.Frame):
    def __init__(self, tool_data, **kwargs):
        super().__init__(**kwargs, relief="groove", borderwidth=5)

        self.tool_data = tool_data

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(layout="constrained")

        # Create data block label for the internal frame
        self.label = tk.Label(
            master=self,
            text="Data Pending...",
            justify="center",
            relief="raised",
            font=("Arial", 16),
            bg="#aeaeae",
        )

        self.label.grid(row=0, column=0, sticky="NSEW")

    def refresh(self):
        years = list(map(str, list(self.tool_data["file_data"])))[::-1]

        values = {"gross income": [], "net income": []}
        for year in years:
            values["gross income"].append(
                round(
                    self.tool_data["file_data"][int(year)].year_income_info[
                        "Gross Income"
                    ]
                    / 1000,
                    2,
                )
            )
            values["net income"].append(
                round(
                    self.tool_data["file_data"][int(year)].year_income_info[
                        "Net Income"
                    ]
                    / 1000,
                    2,
                )
            )

        x = np.arange(len(years))
        width = 0.4
        multiplier = 0

        for attribute, measurement in values.items():
            offset = width * multiplier
            rects = self.ax.barh(x + offset, measurement, width, label=attribute)
            self.ax.bar_label(rects, padding=3)
            multiplier += 1

        def format(y, pos):
            return f"${y:.0f}K"

        self.ax.yaxis.set_major_formatter(FuncFormatter(format))
        self.ax.set_xlabel("Thousands of Dollars")
        self.ax.set_title("Yearly Gross vs Net Income")
        self.ax.set_yticks(x + 0.5 * width, years)
        self.ax.legend(loc="best", ncols=2)
        self.ax.set_xlim(0, max(values["gross income"]) + 20)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="NSEW")
