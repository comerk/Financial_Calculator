from datetime import date
from Income_Information_lib import Pay_Slip


def test_pay_slip_creation() -> None:
    pay_slip = Pay_Slip(
        {"Payment Date": date(2022, 8, 7), "Gross Amount": 1500, "Net Amount": 1000}
    )
    assert pay_slip.pay_date == date(2022, 8, 7)
    assert pay_slip.pay_slip_info["Gross Income"] == 1500
    assert pay_slip.pay_slip_info["Net Income"] == 1000


def test_pay_slip_calculated_values() -> None:
    pay_slip = Pay_Slip(
        {"Payment Date": date(2022, 8, 7), "Gross Amount": 1500, "Net Amount": 1000}
    )
    assert pay_slip.pay_slip_info["Taxed Amount"] == 500
    assert pay_slip.pay_slip_info["Percent Taxed"] == round(500 / 1500, 3)
