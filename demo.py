import numpy as np

x = np.loadtxt(r'C:\Users\fpl11\Desktop\2538.csv', delimiter=',')
hor = x[:, 0]
ver = x[:, 1]
data = []
i = 0
for item in hor[:2048]:
    data.append(str({'y': str(i), 'item1': item}).replace("'y'", "y").replace("'item1'", 'item1') + ',')
    i = i + 1

fl = open(r'C:\Users\fpl11\Desktop\hor.txt', 'w')
for i in data:
    fl.write(i)
    fl.write("\n")
fl.close()

data = []
i = 0
for item in ver[:2048]:
    data.append(str({'y': str(i), 'item1': item}).replace("'y'", "y").replace("'item1'", 'item1') + ',')
    i = i + 1

fl = open(r'C:\Users\fpl11\Desktop\ver.txt', 'w')
for i in data:
    fl.write(i)
    fl.write("\n")
fl.close()

import os

ROOT_PATH = r"G:\BaiduNetdiskDownload\XJTU-SY_Bearing_Datasets\XJTU-SY_Bearing_Datasets\40Hz10kN\Bearing3_1"
dir = sorted(os.listdir(ROOT_PATH),key=lambda i:int(i.split(".")[0]))
data = []
i = 0
for item in dir:
    x = np.loadtxt(ROOT_PATH + r'\\' + item, delimiter=',', skiprows=1)
    hor = x[1:, 0]
    ver = x[1:, 1]
    data.append(
        str({'period': str(i), 'hor': np.max(hor), 'ver': np.max(ver)}).replace("'period'", "period").replace("'hor'",
                                                                                                              'hor').replace(
            "'ver'", 'ver') + ',')
    i = i+1
    print(i)

fl = open(r'C:\Users\fpl11\Desktop\indextrend.txt', 'w')
for i in data:
    fl.write(i)
    fl.write("\n")
fl.close()

fl = open(r'C:\Users\fpl11\Desktop\true.txt', 'w')
for i in true:
    fl.write(str(i))
    fl.write(",")
fl.close()