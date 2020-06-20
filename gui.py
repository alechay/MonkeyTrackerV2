from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import os

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
        self.l1 = QLabel("Weight (kg):")
        self.input_weight = QLineEdit()
        self.l2 = QLabel("Water (ml):")
        self.input_water = QLineEdit()
        self.l3 = QLabel("Fruit?")
        self.button_group = QButtonGroup()
        self.yes = QRadioButton("Yes")
        self.button_group.addButton(self.yes, 1)
        self.no = QRadioButton("No")
        self.button_group.addButton(self.no, 2)
        self.button_group.buttonClicked[int].connect(self.on_button_clicked)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submitMethod)

        self.layout.addWidget(self.date, 0, 0)
        self.layout.addWidget(self.day, 1, 0)
        self.layout.addWidget(self.l1, 2, 0)
        self.layout.addWidget(self.input_weight, 3, 0)
        self.layout.addWidget(self.l2, 4, 0)
        self.layout.addWidget(self.input_water, 5, 0)
        self.layout.addWidget(self.l3, 6, 0)
        self.layout.addWidget(self.yes, 7, 0)
        self.layout.addWidget(self.no, 8, 0)
        self.layout.addWidget(self.submit_button, 9, 0)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def get_day(self):       
        datetimeFormat = '%Y-%m-%d'
        today = datetime.date.today()
        today1 = today.strftime("%B %d, %Y")
        today2 = today.strftime(datetimeFormat)

        # read csv
        first_date = "2020-06-18"
        if first_date == "":
            date = datetime.date.today()
            date1 = date.strftime(datetimeFormat)
        else:
            date = datetime.datetime.strptime(first_date, datetimeFormat).date()
            date1 = date.strftime(datetimeFormat)
        
        diff = today - date
        diff1 = diff.days + 1
        
        return today1, diff1, today2

    def submitMethod(self):
        if os.path.exists("aero.xlsx"):
            print(self.today2, self.diff)
        else:
            print("doesnt exist")

    def on_button_clicked(self, id):
        for button in self.button_group.buttons():
            if button is self.button_group.button(id):
                print(button.text() + " Was Clicked ")

app = QApplication([])
mainWin = MainWindow()
mainWin.show()
app.exec_()