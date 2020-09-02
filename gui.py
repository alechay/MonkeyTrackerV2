from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import os
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.dates as mdates


register_matplotlib_converters()
dirname = os.path.dirname(os.path.realpath(__file__))

def get_day():       
    datetimeFormat = '%Y-%m-%d'
    today = datetime.date.today()
    today1 = today.strftime("%B %d, %Y")
    today2 = today.strftime(datetimeFormat)

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

def repeat_day():
    today, diff, today2 = get_day()
    if os.path.exists(f"{dirname}/aero.xlsx"):
        reader = pd.read_excel(f"{dirname}/aero.xlsx")
        return today2 in list(reader['Date'])

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_data():
    if os.path.exists(f"{dirname}/aero.xlsx"):
        reader = pd.read_excel(f"{dirname}/aero.xlsx")
        return reader

def get_missing_days(data):
    dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in data['Date']]
    date_set = set(dates[0] + datetime.timedelta(x) for x in range((dates[-1] - dates[0]).days))
    missing_dates = sorted(date_set - set(dates))
    days = np.array(data['Day'])
    missing_days = [x for x in range(days[0], days[-1]+1) if x not in days]
    ixs = [list(days).index(days[days < x].max()) + 1 for x in missing_days]
    return missing_dates, missing_days, ixs

def plot_data():
    data = get_data()
    water_f = [data["Water"][i] for i in range(len(data)-1) if 
    
    data['Fruit'][i] == 'Yes' 
    and np.isnan(data["Weight"][i])==False 
    and np.isnan(data["Weight"][i+1])==False 
    and np.isnan(data["Water"][i])==False 
    and data['Day'][i]+1 == data['Day'][i+1]]
    
    chng_weight_f = [data["Weight"][i+1]-data["Weight"][i] for i in range(len(data)-1) if 
    data['Fruit'][i] == 'Yes' 
    and np.isnan(data["Weight"][i])==False 
    and np.isnan(data["Weight"][i+1])==False
    and np.isnan(data["Water"][i])==False  
    and data['Day'][i]+1 == data['Day'][i+1]]

    water_nf = [data["Water"][i] for i in range(len(data)-1) if 
    data['Fruit'][i] == 'No' 
    and np.isnan(data["Weight"][i])==False
    and np.isnan(data["Weight"][i+1])==False
    and np.isnan(data["Water"][i])==False  
    and data['Day'][i]+1 == data['Day'][i+1]]

    chng_weight_nf = [data["Weight"][i+1]-data["Weight"][i] for i in range(len(data)-1) if 
    data['Fruit'][i] == 'No' 
    and np.isnan(data["Weight"][i])==False
    and np.isnan(data["Weight"][i+1])==False
    and np.isnan(data["Water"][i])==False 
    and data['Day'][i]+1 == data['Day'][i+1]]

    if water_f != []:
        m1, b1 = np.polyfit(water_f, chng_weight_f, 1)
    else:
        m1, b1 = (None, None)
    if water_nf != []:
        m2, b2 = np.polyfit(water_nf, chng_weight_nf, 1)
    else:
        m2, b2 = (None, None)
    return water_f, chng_weight_f, water_nf, chng_weight_nf, m1, b1, m2, b2

def check_data_valid():
    if os.path.exists(f"{dirname}/aero.xlsx"):
        data = get_data()
        datetimeFormat = '%Y-%m-%d'
        dates = [datetime.datetime.strptime(d, datetimeFormat) for d in data["Date"]]
        if dates != sorted(dates):
            alert = QMessageBox()
            alert.setText("Problem with the data")
            alert.setInformativeText("The dates are out of order. Please fix in the Excel sheet. Closing the GUI.")
            alert.exec_()
            app.quit()
        elif data["Date"].duplicated().any() or data["Day"].duplicated().any():
            alert = QMessageBox()
            alert.setText("Problem with the data")
            alert.setInformativeText("There are duplicate dates/days. Please fix in the Excel sheet. Closing the GUI.")
            alert.exec_()
            app.quit()
        else:
            pass

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
        self.button2.clicked.connect(self.enterMissingData)
        self.button3 = QPushButton("View table data")
        self.button3.clicked.connect(self.viewTable)
        self.button4 = QPushButton("Daily weight/water")
        self.button4.clicked.connect(self.DailyWaterWeight)
        self.button5 = QPushButton("Daily weight")
        self.button5.clicked.connect(self.WaterPointSize)
        self.button6 = QPushButton("Recommended intake")
        self.button6.clicked.connect(self.RecommendedIntake)
        self.button7 = QPushButton("Info / specs")
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
        check_data_valid()
        repeated = repeat_day()
        if repeated == True:
            self.alert = QMessageBox()
            self.alert.setText("Entry has already been submitted for today")
            self.alert.exec_()
        else:
            self.nextWin = EnterData()
            self.nextWin.show()

    def viewTable(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            self.nextWin = ViewTable()
            self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()

    def DailyWaterWeight(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            self.nextWin = DailyWeightWater()
            self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()            

    def WaterPointSize(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            self.nextWin = WaterPointSize()
            self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()            

    def RecommendedIntake(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            self.nextWin = RecommendedIntake()
            self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()             

    def infoSpecs(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            self.nextWin = InfoSpecs()
            self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()              

    def enterMissingData(self):
        check_data_valid()
        if os.path.exists(f"{dirname}/aero.xlsx"):
            data = get_data()
            missing_dates, missing_days, ixs = get_missing_days(data)
            if missing_dates == []:
                self.alert = QMessageBox()
                self.alert.setText("No missing days")
                self.alert.exec_()
            else:
                self.nextWin = EnterMissingData()
                self.nextWin.show()
        else:
            self.alert = QMessageBox()
            self.alert.setText("No data")
            self.alert.exec_()             

class EnterData(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Enter Data")
        self.widget = QWidget()
        self.layout = QGridLayout()

        self.today, self.diff, self.today2 = get_day()
        self.date = QLabel(f"Today is {self.today}")
        self.day = QLabel(f"Day {self.diff}")
        self.check = QLabel()
        if repeat_day() == True:
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

    def is_toggled(self):
        if self.yes.isChecked() == True and self.no.isChecked() == False:
            fruit = "Yes"
        elif self.yes.isChecked() == False and self.no.isChecked() == True:
            fruit = "No"
        else:
            fruit = None
        return fruit

    def fruit_error(self):
        self.alert = QMessageBox()
        self.alert.setText("Radio box unchecked")
        self.alert.exec_()

    def valid_num_error(self):
        self.alert = QMessageBox()
        self.alert.setText("Enter valid number")
        self.alert.exec_()

    def excel_writer(self, df):
        df["Weight"] = pd.to_numeric(df["Weight"])
        df["Water"] = pd.to_numeric(df["Water"])
        writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        self.close()

    def submitMethod(self):
        date = self.today2
        day = self.diff
        weight = self.input_weight.text()
        water = self.input_water.text()
        fruit = self.is_toggled()
        df = pd.DataFrame(
        {'Date': [date],
        'Day': [day],
        'Weight': [weight],
        'Water': [water],
        'Fruit': [fruit]})
        if os.path.exists(f"{dirname}/aero.xlsx"):
            reader = pd.read_excel(f"{dirname}/aero.xlsx")
            if self.today2 in list(reader['Date']):
                self.alert = QMessageBox()
                self.alert.setText("Entry has already been submitted for this date")
                self.alert.exec_()
                self.close()
            elif fruit == None:
                self.fruit_error()                
            elif df["Weight"][0] == '' or df['Water'][0] == '':
                self.excel_writer(df)
            else:
                if is_float(weight)==False or is_float(water)==False:
                    self.valid_num_error()
                else:
                    df["Weight"] = pd.to_numeric(df["Weight"])
                    df["Water"] = pd.to_numeric(df["Water"])
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
                self.fruit_error()  
            elif df["Weight"][0] == '' or df['Water'][0] == '':
                self.excel_writer(df)
            else:
                if is_float(weight)==False or is_float(water)==False:
                    self.valid_num_error()
                else:
                    self.excel_writer(df)

class EnterMissingData(QMainWindow):

    def __init__(self):
        super().__init__()
        self.display()

    def display(self):
        self.setWindowTitle("Enter missing data")
        self.widget = QWidget()
        self.layout = QGridLayout()

        data = get_data()
        dates, days, ixs = get_missing_days(data)

        self.l1 = QLabel("Select date to add")
        self.date = QComboBox()
        for i in range(len(dates)):
            try:
                self.date.addItem(f"Day {days[i]}, {dates[i]}")
            except IndexError:
                self.alert = QMessageBox()
                self.alert.setText("Problem with the data")
                self.alert.setInformativeText("The dates and day numbers are mismatched. Please fix in the Excel sheet. Closing the GUI.")
                self.alert.exec_()
                self.close()
                app.quit() 
        self.l2 = QLabel("Weight (kg):")
        self.input_weight = QLineEdit()
        self.l3 = QLabel("Water (ml):")
        self.input_water = QLineEdit()
        self.l4 = QLabel("Fruit?")
        self.yes = QRadioButton("Yes")
        self.no = QRadioButton("No")
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_method)

        self.layout.addWidget(self.l1, 0, 0)
        self.layout.addWidget(self.date, 1, 0)
        self.layout.addWidget(self.l2, 2, 0)
        self.layout.addWidget(self.input_weight, 3, 0)
        self.layout.addWidget(self.l3, 4, 0)
        self.layout.addWidget(self.input_water, 5, 0)
        self.layout.addWidget(self.l4, 6, 0)
        self.layout.addWidget(self.yes, 7, 0)
        self.layout.addWidget(self.no, 8, 0)
        self.layout.addWidget(self.submit_button, 9, 0)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def is_toggled(self):
        if self.yes.isChecked() == True and self.no.isChecked() == False:
            fruit = "Yes"
        elif self.yes.isChecked() == False and self.no.isChecked() == True:
            fruit = "No"
        else:
            fruit = None
        return fruit

    def fruit_error(self):
        self.alert = QMessageBox()
        self.alert.setText("Radio box unchecked")
        self.alert.exec_()

    def valid_num_error(self):
        self.alert = QMessageBox()
        self.alert.setText("Enter valid number")
        self.alert.exec_()

    def check_continue(self):
        data = get_data()
        dates, days, ixs = get_missing_days(data)
        if dates != []:
            self.nextWin = EnterMissingData()
            self.nextWin.show()

    def Insert_row(self, row_number, df, row_value): 
        # Starting value of upper half 
        start_upper = 0
        # End value of upper half 
        end_upper = row_number 
        # Start value of lower half 
        start_lower = row_number 
        # End value of lower half 
        end_lower = df.shape[0] 
        # Create a list of upper_half index 
        upper_half = [*range(start_upper, end_upper, 1)] 
        # Create a list of lower_half index 
        lower_half = [*range(start_lower, end_lower, 1)] 
        # Increment the value of lower half by 1 
        lower_half = [x.__add__(1) for x in lower_half] 
        # Combine the two lists 
        index_ = upper_half + lower_half 
        # Update the index of the dataframe 
        df.index = index_ 
        # Insert a row at the end 
        df.loc[row_number] = row_value 
        # Sort the index labels 
        df = df.sort_index() 
        # return the dataframe 
        return df 

    def submit_method(self):
        data = get_data()
        dates, days, ixs = get_missing_days(data)
        i = self.date.currentIndex()
        date = dates[i].strftime('%Y-%m-%d')
        day = days[i]
        weight = self.input_weight.text()
        water = self.input_water.text()
        fruit = self.is_toggled()
        if fruit == None:
            self.fruit_error()
        elif weight == '' or water == '':
            df = pd.DataFrame(
            {'Date': [date],
            'Day': [day],
            'Weight': [weight],
            'Water': [water],
            'Fruit': [fruit]})
            df["Weight"] = pd.to_numeric(df["Weight"])
            df["Water"] = pd.to_numeric(df["Water"])
            row_value = list(df.iloc[0])
            new = self.Insert_row(ixs[i], data, row_value)
            writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='xlsxwriter')
            new.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
            self.close()
            self.check_continue()
        else:
            if is_float(weight)==False or is_float(water)==False:
                self.valid_num_error()
            else: 
                row_value = [date, day, float(weight), float(water), fruit]
                new = self.Insert_row(ixs[i], data, row_value)
                writer = pd.ExcelWriter(f"{dirname}/aero.xlsx", engine='xlsxwriter')
                new.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
                self.close()
                self.check_continue()

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

    def get_interval(self, dates):
        if len(dates) < 3:
            interval = 1
        else:
            interval = len(dates)//3
        return interval
    
    def display(self):
        self.setWindowTitle("Change in Weight and Water")
        data = get_data()
        dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in data['Date']]
        formatter = mdates.DateFormatter("%m/%d/%y")
        interval = self.get_interval(dates)
        locator = mdates.DayLocator(interval=interval)
        
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

    def get_interval(self, dates):
        if len(dates) < 3:
            interval = 1
        else:
            interval = len(dates)//3
        return interval

    def display(self):
        self.setWindowTitle("Change in Weight")
        data = get_data()
        data["Water"] = data["Water"].fillna(0)
        dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in data['Date']]
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.fig.suptitle("Change in Weight and Water", fontsize=16)

        ax1 = sc.fig.add_subplot(111)
        formatter = mdates.DateFormatter("%m/%d/%y")
        ax1.xaxis.set_major_formatter(formatter)
        interval = self.get_interval(dates)
        locator = mdates.DayLocator(interval=interval)
        ax1.xaxis.set_major_locator(locator)
        ax1.plot(dates, data['Weight'], '--r')
        scatter = ax1.scatter(dates, data['Weight'], s=data["Water"], color='r')
        ax1.set_title("Weight vs Day")
        ax1.set_ylabel("Weight (kg)")
        handles, labels = scatter.legend_elements(prop="sizes", num=3, alpha=0.6)
        ax1.legend(handles, labels, loc="center left", title="Water (ml)", bbox_to_anchor=(1, 0.5), labelspacing=2)

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
        ax1.set_xlabel("Water (ml)")
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