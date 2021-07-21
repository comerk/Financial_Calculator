from datetime import date
from dataclasses import dataclass
import pandas as pd

path = "C:/Users/Kameron/OneDrive/Desktop/Test/Kameron_Comer.xlsx"

@dataclass
class Payslip:
    pay_date: pd.Timestamp
    gross_income: float
    net_income: float
    taxed_amount: float
    percent_taxed: float


def get_payslip(data) -> Payslip:

    gross_income = round(data["Gross Amount"],2)
    net_income = round(data["Net Amount"],2)
    taxed_amount = round(gross_income-net_income,2)
    percent_taxed = round(taxed_amount/gross_income*100,2)

    return Payslip(
        pay_date=data["Payment Date"],
        gross_income=gross_income,
        net_income=net_income,
        taxed_amount= taxed_amount,
        percent_taxed=percent_taxed
    )
@dataclass
class Quarter:
    quarter: str
    quarter_gross_income: float = 0
    quarter_net_income: float = 0
    quarter_taxed_amount: float = 0
    quarter_percent_taxed: float = 0
    quarter_payslips = []

    def add_payslip(self, payslip):
        self.quarter_payslips.append(payslip)

        self.quarter_gross_income += payslip.gross_income
        self.quarter_net_income += payslip.net_income

        self.quarter_taxed_amount = (
            self.quarter_gross_income-self.quarter_net_income
        )

        self.quarter_percent_taxed = (
            self.quarter_taxed_amount/self.quarter_gross_income
        )

@dataclass
class Taxable_Year:
    
    year: int
    year_payslips = []
    year_quarters = {}
    annual_gross_income: float = 0
    annual_net_income: float = 0
    annual_taxed_amount: float = 0
    annual_taxed_precent: float = 0

    def add_payslip(self,payslip):
        self.year_payslips.append(payslip)

        self.annual_gross_income += payslip.gross_income
        self.annual_net_income += payslip.net_income

        self.annual_taxed_amount = (
            self.annual_gross_income-self.annual_net_income
        )

        self.annual_taxed_precent = (
            self.annual_taxed_amount/self.annual_gross_income
        )

        self.add_payslip_to_quarter(payslip)

    def add_payslip_to_quarter(self, payslip):

        quarter_dates = {
            "Q1":[date(2021,1,1),date(2021,3,31)],
            "Q2":[date(2021,4,1),date(2021,6,30)],
            "Q3":[date(2021,7,1),date(2021,9,30)],
            "Q4":[date(2021,10,1),date(2021,12,31)]
            }

        for quarter in quarter_dates:
                if (payslip.pay_date >= quarter_dates[quarter][0] and 
                    payslip.pay_date <= quarter_dates[quarter][1]):
                        
                    if quarter not in self.year_quarters:
                        self.year_quarters[quarter] = Quarter(quarter)
                        self.year_quarters[quarter].add_payslip(payslip)
                    else:
                        self.year_quarters[quarter].add_payslip(payslip)


def Sort_Data_Into_Years(raw_data) -> list:
    taxable_years = {}

    for row in range(1, raw_data.shape[0], 1) :
        payslip = get_payslip(raw_data.loc[row])

        if payslip.pay_date.year not in taxable_years.keys():

            taxable_years[payslip.pay_date.year] = (
                Taxable_Year(
                    year=payslip.pay_date.year,
                )
            )
            taxable_years[payslip.pay_date.year].add_payslip(payslip)

        else:
            taxable_years[payslip.pay_date.year].add_payslip(payslip)

    return taxable_years

def import_income_data():
    income_data = pd.read_excel(path, skiprows=1)
    return Sort_Data_Into_Years(income_data)
