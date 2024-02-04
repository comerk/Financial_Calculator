import tkinter as tk


class City_Tax_Frame(tk.Frame):
    def __init__(self, tool_data, **kargs):
        super().__init__(**kargs, relief="raised", borderwidth=5)

        self.tool_data = tool_data

        # Configure city tax frame grid
        self.rowconfigure(0, weight=0, minsize=75)
        self.rowconfigure(1, weight=0, minsize=70)
        self.columnconfigure(0, weight=1, minsize=200)

        # Configure city tax rate scale
        self.city_tax_rate_scl = tk.Scale(
            master=self,
            from_=0,
            to=25,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="City Tax %:",
            borderwidth=2,
            bg="#c4d6e7",
        )
        self.city_tax_rate_scl.grid(row=0, column=0, sticky="NSEW")
        self.city_tax_rate_scl.bind("<ButtonRelease-1>", self.refresh)

        # Configure city tax lable
        self.city_tax_lbl = tk.Label(
            master=self,
            text="Data Pending...",
            relief="ridge",
            font=("Arial", 16),
            bg="#e7c4c4",
        )
        self.city_tax_lbl.grid(row=1, column=0, sticky="NSEW")

    # Refreshes data in the city tax frame for the quarter and tax percent selected
    def refresh(self, *args):
        quarter_gross = self.tool_data["info_frm_ref"].data_sources["Blocks"][1]["text"]

        if quarter_gross != "Data Pending...":
            disallowed_chars = ["$", ","]
            for disallowed_char in disallowed_chars:
                quarter_gross = quarter_gross.replace(disallowed_char, "")

            quarter_city_taxes = round(
                (self.city_tax_rate_scl.get() / 100) * float(quarter_gross), 2
            )
            self.city_tax_lbl.configure(text=f"${quarter_city_taxes}")
        else:
            self.city_tax_lbl.configure(text="Data Pending...")
