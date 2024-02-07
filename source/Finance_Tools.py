from tools.Income_And_Local_Tax_Tool import Income_And_Local_Tax_Tool

app = Income_And_Local_Tax_Tool()
app.protocol("WM_DELETE_WINDOW", app.close)
app.mainloop()
