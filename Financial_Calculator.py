
#import pandas as pd

import os
import re
import Income_Information_lib as Income_Info

file_path = r"C:\Users\Kameron\OneDrive\Desktop\Test\Kameron_Comer.xlsx"

taxable_years = Income_Info.Import_Income_Data(file_path)

for year in taxable_years:
    taxable_years[year].Update_Taxable_Year()
    print(taxable_years[year])
