# Income And Local Tax Calculator
<p align="center">
  <img width="400" height="400" src="https://user-images.githubusercontent.com/59189020/130250588-5822fd66-69de-4cea-bc11-2a2960623580.png">
</p>

## Setup
### Create Virtual Environment (Optional)
If you do not want to install all of the project's dependencies directly to your local machine's python environment you can create a virtual environment using the virtualenv package. 

To install virtualenv for your machine's local python environment:
```
$ pip install virtualenv
```
Now the package is installed, create a virtual environment to install the projects dependecies and execute the script from:
```
$ python3 -m venv /path/to/new/virtual/environment
```
To activate the virtual environment in a terminal instance:
```
$ source ./venv/Scripts/activate
```
To exit the virtual environment:
```
$ deactivate
```
All commands in that terminal instance will execute from the newly created virtual environment after it is activated up until it is eather closed or the deactivate command is given.
### Install Project Dependencies
To install all required dependencies needed to execute the script:
```
$ pip install -r requirments.txt
```
- **Note:** Currently some dependencies do **NOT** support **Python 3.10**, **Python 3.9.6** has been **CONFIRMED** to work with all dependencies found in requirment.txt
## Launch Application
There are three seperate python source files in the project:
 - Income_And_Local_Tax_Calculator.py
 - GUI_lib.py
 - Income_Information_lib.py
 
The source file Income_And_Local_Tax_Calculator is dependent on the other two source files to execute. The GUI_lib source file is used to setup the GUI that the user will interact with, while the Income_Information_lib source file is used to inport the excel file containing the payment information.

To launch the application from the project directory:
```
$ python ./Source/Income_And_Local_Tax_Calculator.py
```
 
## How The Calculator Works
1. Click the "Browse Files" button in the top right corner of the application window
2. Navigate to the excel file exported from the workday website you would like to import (See Note On Alternative)
3. Click the "Open" button in the bottom right corner of your file explorer
4. Select the year that you would like to view in the "Select A Year To View" dropdown. The "Year" data fields will then populate with that years data
5. Select the quarter of the year your selected to view in the "Select A Quarter to View" dropdown. The "Quarter" data fields will then populate with that quarters data
6. Select the amount your particular city taxes you based on your income by using the slider in the right corner of the application window. After a percentage is selected the tax amount owed to your city for that quarter will be displayed under the slider.

<p align="center">
  <img src="https://user-images.githubusercontent.com/59189020/135364060-6e88a8bb-b325-4c3e-835e-5c5f06f18cfa.png">
</p>



---
**Note**
This application was built to import the excel files exported from the workday website, however, any excel file with the following column and data formatting should be handled by the application.
|Payment Date|Gross Amount|Net Amount|
| ---------- | ---------- | -------- |
| yyyy-mm-dd |   Number   |  Number  |

---