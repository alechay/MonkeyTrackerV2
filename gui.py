from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import os
import pandas as pd
from openpyxl import load_workbook

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Main Window")
        self.widget = QWidget()
        self.layout = QGridLayout()
        
        self.button1 = QPushButton("Enter data")
        self.button1.clicked.connect(self.enterData)
        self.button2 = QPushButton("Edit table data")
        # self.button2.clicked.connect(self.onClick)
        self.button3 = QPushButton("Daily weight and daily water")
        # self.button3.clicked.connect(self.onClick)
        self.button4 = QPushButton("Daily weight, dot size = daily water")
        # self.button4.clicked.connect(self.onClick)
        self.button5 = QPushButton("Info and specs")
        # self.button5.clicked.connect(self.onClick)

        self.layout.addWidget(self.button1, 0, 0)
        self.layout.addWidget(self.button2, 1, 0)
        self.layout.addWidget(self.button3, 2, 0)
        self.layout.addWidget(self.button4, 3, 0)
        self.layout.addWidget(self.button5, 4, 0)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def enterData(self):
        self.nextWin = EnterData()
        self.nextWin.show()

class EnterData(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Enter Data")
        self.widget = QWidget()
        self.layout = QGridLayout()

        self.today, self.diff, self.today2 = self.get_day()
        self.date = QLabel(f"Today is {self.today}")
        self.day = QLabel(f"Day {self.diff}")
        self.check = QLabel()
        if self.repeat_day() == True:
            self.check.setText("Entry has already been submitted for this date")
            self.check.setStyleSheet("color: red;")
        self.l1 = QLabel("Weight (kg):")
        self.input_weight = QLineEdit()
        self.l2 = QLabel("Water (ml):")
        self.input_water = QLineEdit()
        self.l3 = QLabel("Fruit?")
        self.yes = QRadioButton("Yes")
        self.no = QRadioButton("No")
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submitMethod)

        self.layout.addWidget(self.date, 0, 0)
        self.layout.addWidget(self.day, 1, 0)
        self.layout.addWidget(self.check, 2, 0)
        self.layout.addWidget(self.l1, 3, 0)
        self.layout.addWidget(self.input_weight, 4, 0)
        self.layout.addWidget(self.l2, 5, 0)
        self.layout.addWidget(self.input_water, 6, 0)
        self.layout.addWidget(self.l3, 7, 0)
        self.layout.addWidget(self.yes, 8, 0)
        self.layout.addWidget(self.no, 9, 0)
        self.layout.addWidget(self.submit_button, 10, 0)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def get_day(self):       
        datetimeFormat = '%Y-%m-%d'
        today = datetime.date.today()
        today1 = today.strftime("%B %d, %Y")
        today2 = today.strftime(datetimeFormat)

        dirname = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(f"{dirname}/aero.xlsx"):
            reader = pd.read_excel(f'{dirname}/aero.xlsx')
            first_date = reader['Date'][0]
            date = datetime.datetime.strptime(first_date, datetimeFormat).date()
            # date1 = date.strftime(datetimeFormat)
        else:
            date = datetime.date.today()
            # date1 = date.strftime(datetimeFormat)
        
        diff = today - date
        diff1 = diff.days + 1
        
        return today1, diff1, today2

    def submitMethod(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        fruit = self.is_toggled()
        df = pd.DataFrame(
        {'Date': [self.today2],
        'Day': [self.diff],
        'Weight': [self.input_weight.text()],
        'Water': [self.input_water.text()],
        'Fruit': [fruit]})
        if os.path.exists(f"{dirname}/aero.xlsx"):
            reader = pd.read_excel(f"{dirname}/aero.xlsx")
            if self.today2 in list(reader['Date']):
                self.alert = QMessageBox()
                self.alert.setText("Entry has already been submitted for this date")
                self.alert.exec_()
            elif fruit == None:
                self.alert = QMessageBox()
                self.alert.setText("Check 1 radio box")
                self.alert.exec_()
            else:
                writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='openpyxl')
                # try to open an existing workbook
                writer.book = load_workbook(f"{dirname}/aero.xlsx")
                # copy existing sheets
                writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
                # write out the new sheet
                df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)
                writer.close()
        else:
            if fruit == None:
                self.alert = QMessageBox()
                self.alert.setText("Check 1 radio box")
                self.alert.exec_()
            else:
                writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
    
    def is_toggled(self):
        if self.yes.isChecked() == True and self.no.isChecked() == False:
            fruit = "Yes"
        elif self.yes.isChecked() == False and self.no.isChecked() == True:
            fruit = "No"
        else:
            fruit = None
        return fruit
    
    def repeat_day(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(f"{dirname}/aero.xlsx"):
            reader = pd.read_excel(f"{dirname}/aero.xlsx")
            return self.today2 in list(reader['Date'])

app = QApplication([])
mainWin = MainWindow()
mainWin.show()
app.exec_()