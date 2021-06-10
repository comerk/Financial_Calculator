
import csv
import os
import re
import time
from datetime import date

path = r"C:\Users\Kameron.Comer\OneDrive - Gentex Corporation\Desktop\Test"
quarters = {"Q1":[date(2021,1,1),date(2021,3,31)],
            "Q2":[date(2021,4,1),date(2021,6,30)],
            "Q3":[date(2021,7,1),date(2021,9,30)],
            "Q4":[date(2021,10,1),date(2021,12,31)]}

class Pay_Slip:
    def __init__(self,data):
        self.pay_date = date(int(re.search(r"\d{2,4}$",data["Payment Date"]).group(0)),
                             int(re.search(r"^\d{1,2}",data["Payment Date"]).group(0)),
                             int(re.search(r"\d{1,2}(?=\/\d{4})",data["Payment Date"]).group(0)))

        self.pay_slip_stats = {"Gross Income": float, "Net Income": float,"Taxed Amount": float,"Percent Taxed": float}

        self.pay_slip_stats["Gross Income"] = round(float(data["Gross Amount"].replace(',','')),2)
        self.pay_slip_stats["Net Income"] = round(float(data["Net Amount"].replace(',','')),2)
        self.pay_slip_stats["Taxed Amount"] = round(self.pay_slip_stats["Gross Income"] - self.pay_slip_stats["Net Income"],2)
        self.pay_slip_stats["Percent Taxed"] = round(self.pay_slip_stats["Taxed Amount"] / self.pay_slip_stats["Gross Income"],3)

    def __str__(self):
        string = f"{self.pay_date}\t"
        for stat in self.pay_slip_stats:
            string += str(self.pay_slip_stats[stat]) + '\t'
        string += '\n'

        return  string

class Quarter:
    def __init__(self,quarter):
        self.quarter = quarter
        self.quarter_stats = {"Gross Income": float, "Net Income": float,"Taxed Amount": float,"Percent Taxed":float}

        self.quarter_stats["Gross Income"] = 0
        self.quarter_stats["Net Income"] = 0
        self.quarter_stats["Taxed Amount"] = 0
        self.quarter_stats["Percent Taxed"] = 0

        self.income_data_for_quarter = []

    def __str__(self):
        self.Update_Income_Values()

        string = f"{self.quarter} Details\n\n"
        for stat in self.quarter_stats:
            string += "Total " + stat + ": " + str(self.quarter_stats[stat]) + "\t"
            if stat == "Net Income" or stat == "Percent Taxed":
                string += '\n'
        string += "_________________________________________________________\n\n"
        string += "Pay Date\tGross\tNet\tTaxed\tTax %\n"

        for pay_slip in self.income_data_for_quarter:
            string += pay_slip.__str__()

        string += "_________________________________________________________\n\n"

        return string

    def Update_Income_Values(self):
        self.quarter_stats["Gross Income"] = 0
        self.quarter_stats["Net Income"] = 0
        self.quarter_stats["Taxed Amount"] = 0
        self.quarter_stats["Percent Taxed"] = 0

        for pay_slip in self.income_data_for_quarter:
            self.quarter_stats["Gross Income"] += pay_slip.pay_slip_stats["Gross Income"]
            self.quarter_stats["Net Income"] += pay_slip.pay_slip_stats["Net Income"]
            self.quarter_stats["Taxed Amount"] += pay_slip.pay_slip_stats["Taxed Amount"]

        self.quarter_stats["Percent Taxed"] = round(self.quarter_stats["Taxed Amount"] / self.quarter_stats["Gross Income"],2)

        self.quarter_stats["Gross Income"] = round(self.quarter_stats["Gross Income"],2)
        self.quarter_stats["Net Income"] = round(self.quarter_stats["Net Income"],2)
        self.quarter_stats["Taxed Amount"] = round(self.quarter_stats["Taxed Amount"],2)

class Taxable_Year:
    def __init__(self,year):
        self.year = year
        self.year_stats = {"Gross Income": float, "Net Income": float,"Taxed Amount": float,"Percent Taxed":float}

        self.year_stats["Gross Income"] = 0
        self.year_stats["Net Income"] = 0
        self.year_stats["Taxed Amount"] = 0
        self.year_stats["Percent Taxed"] = 0

        self.income_data_for_year = []
        self.year_quarters = {}

    def __str__(self):
        string = f"------------------------ Tax Year: {self.year} ------------------------\n\n"
        for stat in self.year_stats:
            string += "   " + "Total " + stat + ": " + str(self.year_stats[stat]) + "\t"
            if stat == "Net Income" or stat == "Percent Taxed":
                string += '\n'
        string += "----------------------------------------------------------------\n\n"
                  
        
        for quarter in self.year_quarters:
            string += self.year_quarters[quarter].__str__()

        string += "----------------------------------------------------------------\n\n"

        return string

    def Add_Pay_Slip_To_Quarter(self, pay_slip):
        for quarter in quarters:
                if pay_slip.pay_date.month >= quarters[quarter][0].month and pay_slip.pay_date.month <= quarters[quarter][1].month:
                    if pay_slip.pay_date.day >= quarters[quarter][0].day and pay_slip.pay_date.day <= quarters[quarter][1].day:
                        if quarter not in self.year_quarters:
                            self.year_quarters[quarter] = Quarter(quarter)
                            self.year_quarters[quarter].income_data_for_quarter.append(pay_slip)
                        else:
                            self.year_quarters[quarter].income_data_for_quarter.append(pay_slip)

    def Update_Income_Values(self):

        self.year_stats["Gross Income"] = 0
        self.year_stats["Net Income"] = 0
        self.year_stats["Taxed Amount"] = 0
        self.year_stats["Percent Taxed"] = 0

        for pay_slip in self.income_data_for_year:
            self.year_stats["Gross Income"] += pay_slip.pay_slip_stats["Gross Income"]
            self.year_stats["Net Income"] += pay_slip.pay_slip_stats["Net Income"]
            self.year_stats["Taxed Amount"] += pay_slip.pay_slip_stats["Taxed Amount"]

        self.year_stats["Percent Taxed"] = round(self.year_stats["Taxed Amount"] / self.year_stats["Gross Income"],3)
        
        self.year_stats["Gross Income"] = round(self.year_stats["Gross Income"],2)
        self.year_stats["Net Income"] = round(self.year_stats["Net Income"],2)
        self.year_stats["Taxed Amount"] = round(self.year_stats["Taxed Amount"],2)

    def Sort_Income_Data_Into_Quarters(self):
        for pay_slip in self.income_data_for_year:
            self.Add_Pay_Slip_To_Quarter(pay_slip)
        
    def Update_Quarters(self):
        for quarter in self.year_quarters:
            self.year_quarters[quarter].Update_Income_Values()

    def Update_Taxable_Year(self):
        self.Update_Income_Values()
        self.Update_Quarters()

def Sort_Data_Into_Years(raw_data):
    taxable_years = {}
    for pay_slip in raw_data:

        try: 
            date_year = re.search(r"\d{2,4}$",pay_slip["Payment Date"]).group(0)
        except:
            return

        if date_year not in taxable_years:
            taxable_years[date_year]=(Taxable_Year(date_year))
            taxable_years[date_year].income_data_for_year.append(Pay_Slip(pay_slip))
        else:
            taxable_years[date_year].income_data_for_year.append(Pay_Slip(pay_slip))
    
    for year in taxable_years:
        taxable_years[year].Sort_Income_Data_Into_Quarters()
        taxable_years[year].Update_Taxable_Year
    return taxable_years

def Import_Income_Data(path):
    os.chdir(path)

    for file in os.listdir():
        print(file)
        if re.match(r'.*\.csv',file):
            
            with open(file,'rb') as input, open("new.csv", 'wb') as output:
                writer = csv.writer(output)
                if csv.reader(input)[0][0] == "Payslips":
                    for row in csv.reader(input)[1:]:
                        writer.writerow(row)

                    os.remove(file)
                    os.rename('new.csv',file)
            
            with open(file,newline='') as file:
                taxable_years = Sort_Data_Into_Years(csv.DictReader(file))


            with open (file, newline='') as f:

                if csv.reader(file)[0][0] == "Payslips":
                    writer.writerow(0)
                

    return taxable_years
            

taxable_years = Import_Income_Data(path)

for year in taxable_years:
    taxable_years[year].Update_Taxable_Year()
    print(taxable_years[year])

