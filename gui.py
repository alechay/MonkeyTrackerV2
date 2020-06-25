from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import datetime
import os
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

def get_data():
    dirname = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(f"{dirname}/aero.xlsx"):
        reader = pd.read_excel(f"{dirname}/aero.xlsx")
        return reader

def plot_data():
    data = get_data()
    water_f = [data["Water"][i] for i in range(len(data)-1) if data['Fruit'][i] == 'Yes' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
    chng_weight_f = [data["Weight"][i]-data["Weight"][i+1] for i in range(len(data)-1) if data['Fruit'][i] == 'Yes' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
    water_nf = [data["Water"][i] for i in range(len(data)-1) if data['Fruit'][i] == 'No' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
    chng_weight_nf = [data["Weight"][i]-data["Weight"][i+1] for i in range(len(data)-1) if data['Fruit'][i] == 'No' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
    if water_f != []:
        m1, b1 = np.polyfit(water_f, chng_weight_f, 1)
    else:
        m1, b1 = (None, None)
    if water_nf != []:
        m2, b2 = np.polyfit(water_nf, chng_weight_nf, 1)
    else:
        m2, b2 = (None, None)
    return water_f, chng_weight_f, water_nf, chng_weight_nf, m1, b1, m2, b2

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

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
        self.button2 = QPushButton("Enter missing data")
        # self.button2.clicked.connect(self.enterData)
        self.button3 = QPushButton("View table data")
        self.button3.clicked.connect(self.viewTable)
        self.button4 = QPushButton("Daily weight/water")
        self.button4.clicked.connect(self.DailyWaterWeight)
        self.button5 = QPushButton("Daily weight")
        self.button5.clicked.connect(self.WaterPointSize)
        self.button6 = QPushButton("Recommended intake")
        self.button6.clicked.connect(self.RecommendedIntake)
        self.button7 = QPushButton("Info & specs")
        self.button7.clicked.connect(self.infoSpecs)

        self.layout.addWidget(self.button1, 0, 0)
        self.layout.addWidget(self.button2, 0, 1)
        self.layout.addWidget(self.button3, 0, 2)
        self.layout.addWidget(self.button4, 1, 0)
        self.layout.addWidget(self.button5, 1, 1)
        self.layout.addWidget(self.button6, 1, 2)
        self.layout.addWidget(self.button7, 2, 1)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def enterData(self):
        self.nextWin = EnterData()
        self.nextWin.show()

    def viewTable(self):
        self.nextWin = ViewTable()
        self.nextWin.show()

    def DailyWaterWeight(self):
        self.nextWin = DailyWeightWater()
        self.nextWin.show()

    def WaterPointSize(self):
        self.nextWin = WaterPointSize()
        self.nextWin.show()

    def RecommendedIntake(self):
        self.nextWin = RecommendedIntake()
        self.nextWin.show()

    def infoSpecs(self):
        self.nextWin = InfoSpecs()
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
                self.close()
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
                self.close()
        else:
            if fruit == None:
                self.alert = QMessageBox()
                self.alert.setText("Check 1 radio box")
                self.alert.exec_()
            else:
                writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
                self.close()
    
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

class ViewTable(QMainWindow):

    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("View Data")
        self.data = get_data()

        self.table = QtWidgets.QTableView()
        self.model = TableModel(self.data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
         
class DailyWeightWater(QMainWindow):

    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Change in Weight and Water")
        data = get_data()
        dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in data['Date']]
        formatter = mdates.DateFormatter("%Y-%m-%d")
        locator = mdates.DayLocator()
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.fig.suptitle("Change in Weight and Water", fontsize=16)
        gs = sc.fig.add_gridspec(2,1)

        ax1 = sc.fig.add_subplot(gs[0,0])
        ax1.xaxis.set_major_formatter(formatter)
        ax1.xaxis.set_major_locator(locator)
        ax1.plot(dates, data['Weight'], '.--r')
        ax1.set_title("Weight vs Day")
        ax1.set_ylabel("Weight (kg)")

        ax2 = sc.fig.add_subplot(gs[1,0])
        ax2.xaxis.set_major_formatter(formatter)
        ax2.xaxis.set_major_locator(locator)
        ax2.plot(dates, data['Water'], '.--b')
        ax2.set_title("Water vs Day")
        ax2.set_ylabel("Water (ml)")

        sc.fig.tight_layout()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)
        
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class WaterPointSize(QMainWindow):

    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Change in Weight")
        data = get_data()
        dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in data['Date']]
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.fig.suptitle("Change in Weight and Water", fontsize=16)

        ax1 = sc.fig.add_subplot(111)
        formatter = mdates.DateFormatter("%Y-%m-%d")
        ax1.xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        ax1.xaxis.set_major_locator(locator)
        ax1.plot(dates, data['Weight'], '--r')
        scatter = ax1.scatter(dates, data['Weight'], s=data["Water"], color='r')
        ax1.set_title("Weight vs Day")
        ax1.set_ylabel("Weight (kg)")
        handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
        ax1.legend(handles, labels, loc="upper right", title="Water (ml)")

        sc.fig.tight_layout()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)
        
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class RecommendedIntake(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Recommended Intake")
        water_f, chng_weight_f, water_nf, chng_weight_nf, m1, b1, m2, b2 = plot_data()

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.fig.suptitle("Change in Weight and Water", fontsize=16)

        ax1 = sc.fig.add_subplot(111)
        ax1.scatter(water_f, chng_weight_f, color='b', label='Fruit')
        ax1.plot(water_f, m1*np.array(water_f)+b1, 'b')
        ax1.scatter(water_nf, chng_weight_nf, color='r', label='No Fruit')
        ax1.plot(water_nf, m2*np.array(water_nf)+b2, 'r')
        ax1.set_title("Amount of water vs change in weight")
        ax1.set_ylabel("Change in Weight (kg)")
        ax1.set_xlabel("Water (ml")
        ax1.legend()

        sc.fig.tight_layout()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)
        
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class InfoSpecs(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Info and specs")
        widget = QWidget()
        layout = QVBoxLayout()

        water_f, chng_weight_f, water_nf, chng_weight_nf, m1, b1, m2, b2 = plot_data()
        
        if m1 == None or b1==None:
            fruit_eq = QLabel("Fruit: N/A")
            fruit = QLabel("")
        else:
            fruit_zero = round(-b1/m1, 2)
            fruit_eq = QLabel(f"Fruit: y={round(m1, 2)}x + {round(b1, 2)}")
            fruit = QLabel(f"If he gets fruit, monkey needs {fruit_zero}ml of water to maintain his weight")

        if m2 == None or b2==None:
            nofruit_eq = QLabel("No Fruit: N/A")
            nofruit = QLabel("")
        else:
            nofruit_zero = round(-b2/m2, 2)
            nofruit_eq = QLabel(f"No fruit: y={round(m2, 2)}x + {round(b2, 2)}")
            nofruit = QLabel(f"If he doesn't get fruit, monkey needs {nofruit_zero}ml of water to maintain his weight")
        
        layout.addWidget(fruit_eq)
        layout.addWidget(fruit)
        layout.addWidget(nofruit_eq)
        layout.addWidget(nofruit)

        widget.setLayout(layout)
        self.setCentralWidget(widget)        

app = QApplication([])
mainWin = MainWindow()
mainWin.show()
app.exec_()