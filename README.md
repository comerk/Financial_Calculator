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



---
**Note**
This application was built to import the excel files exported from the workday website, however, any excel file with the following column and data formatting should be handled by the application.
|Payment Date|Gross Amount|Net Amount|
| ---------- | ---------- | -------- |
| yyyy-mm-dd |   Number   |  Number  |

---
