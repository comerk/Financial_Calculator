import tkinter as tk


class Information_Frame(tk.Frame):
    def __init__(self, **kargs):
        super().__init__(**kargs)

        # Creates tuple of information labels
        data_labels = (
            ["Year Gross Income", "Year Net Income", "Year Taxed Amount"],
            ["Quarter Gross Income", "Quarter Net Income", "Quarter Taxed Amount"],
        )

        # Creates dict where internal frames and their data are stored
        self.data_sources = {"Frames": [], "Blocks": []}

        for row in range(0, 3):
            # Information Frame Grid Setup -> Row
            self.rowconfigure(row, weight=1, minsize=110)
            for col in range(0, 2):
                # Information Frame Grid Setup -> Col
                self.columnconfigure(col, weight=1, minsize=200)

                # Create Frame for one of Information Frame's Grid sectors
                self.data_sources["Frames"].append(tk.Frame(master=self))

                # Setup Internal Frame's own grid
                self.data_sources["Frames"][-1].rowconfigure(0, weight=1, minsize=25)
                self.data_sources["Frames"][-1].rowconfigure(1, weight=5, minsize=75)
                self.data_sources["Frames"][-1].columnconfigure(
                    0, weight=1, minsize=200
                )

                # Create header label for the internal frame
                header_lbl = tk.Label(
                    master=self.data_sources["Frames"][-1],
                    text=data_labels[col][row],
                    justify="center",
                    relief="raised",
                    borderwidth=5,
                    font=("Arial", 12),
                    bg="#FFD700",
                )

                # Create data block label for the internal frame
                self.data_sources["Blocks"].append(
                    tk.Label(
                        master=self.data_sources["Frames"][-1],
                        text="Data Pending...",
                        justify="center",
                        relief="raised",
                        font=("Arial", 16),
                        bg="#aeaeae",
                    )
                )

                # Place header inside internal frame at (0,0)
                header_lbl.grid(row=0, column=0, sticky="NSEW")
                # Place data block inside internal frame at (1,0)
                self.data_sources["Blocks"][-1].grid(row=1, column=0, sticky="NSEW")

                # Assign internal frame to Information Frame's grid at (row,col)
                self.data_sources["Frames"][-1].grid(row=row, column=col, sticky="NSEW")
