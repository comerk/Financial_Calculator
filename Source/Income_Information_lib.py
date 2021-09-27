from datetime import date
import pandas as pd

quarter_dates = {
            "Q1":[date(2021,1,1),date(2021,3,31)],
            "Q2":[date(2021,4,1),date(2021,6,30)],
            "Q3":[date(2021,7,1),date(2021,9,30)],
            "Q4":[date(2021,10,1),date(2021,12,31)]
            }

class Pay_Slip:
    def __init__(self,data):
        self.pay_date = data["Payment Date"]

        self.pay_slip_info = {
            "Gross Income": float,
            "Net Income":   float,
            "Taxed Amount": float,
            "Percent Taxed":float
            }

        self.pay_slip_info["Gross Income"] = round(
            float(data["Gross Amount"]),2
            )

        self.pay_slip_info["Net Income"] = round(
            float(data["Net Amount"]),2
            )

        self.pay_slip_info["Taxed Amount"] = round(
            self.pay_slip_info["Gross Income"] - self.pay_slip_info["Net Income"],2
            )

        self.pay_slip_info["Percent Taxed"] = round(
            self.pay_slip_info["Taxed Amount"] / self.pay_slip_info["Gross Income"],3
            )

    def __str__(self):
        string = f"{self.pay_date}\t"
        for stat in self.pay_slip_info:
            string += str(self.pay_slip_info[stat]) + '\t'
        string += '\n'

        return  string

class Quarter:
    def __init__(self,quarter):
        self.quarter = quarter
        self.quarter_income_info = {
            "Gross Income": float,
            "Net Income": float,
            "Taxed Amount": float,
            "Percent Taxed":float
            }

        self.quarter_income_info["Gross Income"] = 0
        self.quarter_income_info["Net Income"] = 0
        self.quarter_income_info["Taxed Amount"] = 0
        self.quarter_income_info["Percent Taxed"] = 0

        self.income_data_for_quarter = []

    def __str__(self):
        self.Update_Income_Values()

        string = f"{self.quarter} Details\n\n"
        for stat in self.quarter_income_info:
            string += "Total " + stat + ": " + str(self.quarter_income_info[stat]) + "\t"
            if stat == "Net Income" or stat == "Percent Taxed":
                string += '\n'
        string += "_________________________________________________________\n\n"
        string += "Pay Date\tGross\tNet\tTaxed\tTax %\n"

        for pay_slip in self.income_data_for_quarter:
            string += pay_slip.__str__()

        string += "_________________________________________________________\n\n"

        return string

    def Update_Income_Values(self):
        self.quarter_income_info["Gross Income"] = 0
        self.quarter_income_info["Net Income"] = 0
        self.quarter_income_info["Taxed Amount"] = 0
        self.quarter_income_info["Percent Taxed"] = 0

        for pay_slip in self.income_data_for_quarter:
            self.quarter_income_info["Gross Income"] += pay_slip.pay_slip_info["Gross Income"]
            self.quarter_income_info["Net Income"] += pay_slip.pay_slip_info["Net Income"]
            self.quarter_income_info["Taxed Amount"] += pay_slip.pay_slip_info["Taxed Amount"]

        self.quarter_income_info["Percent Taxed"] = round(
            self.quarter_income_info["Taxed Amount"] / self.quarter_income_info["Gross Income"],2
            )
        self.quarter_income_info["Gross Income"] = round(
            self.quarter_income_info["Gross Income"],2
            )
        self.quarter_income_info["Net Income"] = round(
            self.quarter_income_info["Net Income"],2
            )
        self.quarter_income_info["Taxed Amount"] = round(
            self.quarter_income_info["Taxed Amount"],2
            )

class Taxable_Year:
    def __init__(self,year):
        self.year = year
        self.year_income_info = {
            "Gross Income": float,
            "Net Income": float,
            "Taxed Amount": float,
            "Percent Taxed":float
        }

        self.year_income_info["Gross Income"] = 0
        self.year_income_info["Net Income"] = 0
        self.year_income_info["Taxed Amount"] = 0
        self.year_income_info["Percent Taxed"] = 0

        self.pay_slips = []
        self.quarters = {}

    def __str__(self):
        string = f"------------------------ Tax Year: {self.year} ------------------------\n\n"
        for stat in self.year_income_info:
            string += "   " + "Total " + stat + ": " + str(self.year_income_info[stat]) + "\t"
            if stat == "Net Income" or stat == "Percent Taxed":
                string += '\n'
        string += "----------------------------------------------------------------\n\n"
                  
        
        for quarter in self.quarters:
            string += self.quarters[quarter].__str__()

        string += "----------------------------------------------------------------\n\n"

        return string

    def Add_Pay_Slip_To_Quarter(self, pay_slip):
        for quarter in quarter_dates:
                if (pay_slip.pay_date.month >= quarter_dates[quarter][0].month and 
                    pay_slip.pay_date.month <= quarter_dates[quarter][1].month):
                    
                    if (pay_slip.pay_date.day >= quarter_dates[quarter][0].day and 
                        pay_slip.pay_date.day <= quarter_dates[quarter][1].day):
                        
                        if quarter not in self.quarters:
                            self.quarters[quarter] = Quarter(quarter)
                            self.quarters[quarter].income_data_for_quarter.append(pay_slip)
                        else:
                            self.quarters[quarter].income_data_for_quarter.append(pay_slip)

    def Update_Income_Values(self):

        self.year_income_info["Gross Income"] = 0
        self.year_income_info["Net Income"] = 0
        self.year_income_info["Taxed Amount"] = 0
        self.year_income_info["Percent Taxed"] = 0

        for pay_slip in self.pay_slips:
            self.year_income_info["Gross Income"] += pay_slip.pay_slip_info["Gross Income"]
            self.year_income_info["Net Income"] += pay_slip.pay_slip_info["Net Income"]
            self.year_income_info["Taxed Amount"] += pay_slip.pay_slip_info["Taxed Amount"]

        self.year_income_info["Percent Taxed"] = round(
            self.year_income_info["Taxed Amount"] / self.year_income_info["Gross Income"],3
            )
        self.year_income_info["Gross Income"] = round(
            self.year_income_info["Gross Income"],2
            )
        self.year_income_info["Net Income"] = round(
            self.year_income_info["Net Income"],2
            )
        self.year_income_info["Taxed Amount"] = round(
            self.year_income_info["Taxed Amount"],2
            )

    def Sort_Income_Data_Into_Quarters(self):
        for pay_slip in self.pay_slips:
            self.Add_Pay_Slip_To_Quarter(pay_slip)
        
    def Update_Quarters(self):
        for quarter in self.quarters:
            self.quarters[quarter].Update_Income_Values()

    def Update_Taxable_Year(self):
        self.Update_Income_Values()
        self.Update_Quarters()

def Sort_Data_Into_Years(raw_data):
    taxable_years = {}

    for row in range(1, raw_data.shape[0], 1) :
        pay_slip = Pay_Slip(raw_data.loc[row])

        if pay_slip.pay_date.year not in taxable_years.keys():

            taxable_years[pay_slip.pay_date.year] = (
                Taxable_Year(pay_slip.pay_date.year)
                )

            taxable_years[pay_slip.pay_date.year].pay_slips.append(pay_slip)

        else:
            taxable_years[pay_slip.pay_date.year].pay_slips.append(pay_slip)

    for year in taxable_years:
        taxable_years[year].Sort_Income_Data_Into_Quarters()
        taxable_years[year].Update_Taxable_Year()

    return taxable_years

def Import_Income_Data(path):
    income_data = pd.read_excel(path, skiprows=1)
    taxable_years = Sort_Data_Into_Years(income_data)
                
    return taxable_years    
            
