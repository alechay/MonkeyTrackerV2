# import os
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

# def get_data():
#     dirname = os.path.dirname(os.path.realpath(__file__))
#     if os.path.exists(f"{dirname}/aero.xlsx"):
#         reader = pd.read_excel(f"{dirname}/aero.xlsx")
#         return reader

# data = get_data()
# water_f = [data["Water"][i] for i in range(len(data)-1) if data['Fruit'][i] == 'Yes' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
# chng_weight_f = [data["Weight"][i]-data["Weight"][i+1] for i in range(len(data)-1) if data['Fruit'][i] == 'Yes' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
# water_nf = [data["Water"][i] for i in range(len(data)-1) if data['Fruit'][i] == 'No' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
# chng_weight_nf = [data["Weight"][i]-data["Weight"][i+1] for i in range(len(data)-1) if data['Fruit'][i] == 'No' and data["Weight"][i+1]!='' and data['Day'][i]+1 == data['Day'][i+1]]
# print(water_f)
# print(chng_weight_f)
# print(water_nf)
# print(chng_weight_nf)
# water_f = np.array(water_f)
# m1, b1 = np.polyfit(water_f, chng_weight_f, 1)

# plt.scatter(water_f, chng_weight_f, label='fruit')
# plt.plot(water_f, m1*water_f+b1, 'b')
# plt.scatter(water_nf, chng_weight_nf, label='no fruit')
# plt.scatter([11,12], [-1,1], label='random')
# plt.legend()

# plt.show()

from datetime import datetime

date_strs = ['07-06-2010', '06-24-2010', '07-05-2010', '06-25-2010']
date_strs1 = ['06-24-2010', '06-25-2010', '07-05-2010', '07-06-2010']
# date_strs = ['02-29-2012', '02-28-2012', '03-01-2012']
# date_strs = ['01-01-2000']
dates = [datetime.strptime(d, "%m-%d-%Y") for d in date_strs]
dates1 = [datetime.strptime(d, "%m-%d-%Y") for d in date_strs1]

date_ints = set([d.toordinal() for d in dates])

# if len(date_ints) == 1:
#     print("unique")
# elif max(date_ints) - min(date_ints) == len(date_ints) - 1:
#     print("consecutive")
# else:
#     print("not consecutive")

print(dates == sorted(dates))
print(dates1 == sorted(dates1))

df = pd.DataFrame({"a": [1,1,1,1]})
if df["a"].duplicated().any():
    print('yo')