# By Francisco Sanchez
# The file dataCSV has 3 columns with headers
# Column 0: Time; Column 1: Line Current; Column 2: L-N Voltage
# Store csv file in Python directory.
# use file comp_dataCSV.csv for troubleshooting

import xlwt
from xlwt import easyxf
import numpy
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy import signal
input('Welcome to Harmonics Calculations: John Showell Approved\nPlease press Enter to continue')

#csv = np.genfromtxt('dataCSV.csv', delimiter=',', skip_header=1, usecols=(0, 1, 2))
load_fn = 'BRB_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data']

data = data[:, 0]
csv = data[500000:504000]
csv = signal.detrend(csv, type='constant')

#t0 = csv[1:3, 0]
sp = 1/20000
pi = math.pi
f = 50
T = 1 / f
ns = int(round(T / sp))
t = csv[:ns + 1]
dataI = csv[:ns + 1]
l = np.arange(0, T, sp)  # Time Vector

# sum of rows
#avgV = np.mean(dataV[0:ns])
avgI = np.mean(dataI[0:ns])

# rms of rows
#rmsV = np.sqrt(np.mean(dataV[0:ns] ** 2))
rmsI = np.sqrt(np.mean(dataI[0:ns] ** 2))

aI = np.zeros([ns + 1, 101])
bI = np.zeros([ns + 1, 101])
aV = np.zeros([ns + 1, 101])
bV = np.zeros([ns + 1, 101])
AI = np.zeros(101)
BI = np.zeros(101)
AV = np.zeros(101)
BV = np.zeros(101)
ThetaI = np.zeros(101)
ThetaV = np.zeros(101)
FI = np.zeros([ns + 1, 101])
FV = np.zeros([ns + 1, 101])
RMSI = np.zeros(101)
HfI = np.zeros(101)
HrmsI = np.zeros(101)
RMSV = np.zeros(101)
HfV = np.zeros(101)
HrmsV = np.zeros(101)


for n in range(1, 101):
    for m in range(0, ns):
        aI[m, n] = dataI[m] * np.cos(n * t[m] * 2 * pi * f)  # Fourier coefficients I
        bI[m, n] = dataI[m] * np.sin(n * t[m] * 2 * pi * f)
        #aV[m, n] = dataV[m] * np.cos(n * t[m] * 2 * pi * f)  # Fourier coefficients V
        #bV[m, n] = dataV[m] * np.sin(n * t[m] * 2 * pi * f)

for n in range(1, 101):
    AI[n] = sum(aI[:, n]) * 2 / ns  # Calculation of C coefficient; Current (divided by ns)
    BI[n] = sum(bI[:, n]) * 2 / ns
    CI = abs(AI + BI * 1j)

    #AV[n] = sum(aV[:, n]) * 2 / ns  # Calculation of C coefficient; Voltage (divided by ns)
    #BV[n] = sum(bV[:, n]) * 2 / ns
    #CV = abs(AV + BV * 1j)
    if AI[n] > 0:  # Calculation of phase angle; Current
        ThetaI[n] = -math.atan(BI[n] / AI[n])
    else:
        ThetaI[n] = pi - math.atan(BI[n] / AI[n])
    #if AV[n] > 0:
    #    ThetaV[n] = -math.atan(BV[n] / AV[n])  # Calculation of phase angle; Voltage
    #else:
    #    ThetaV[n] = pi - math.atan(BV[n] / AV[n])
    for Ti in range(0, ns):
        FI[Ti, n] = CI[n] * np.cos(n * 2 * pi * f * t[Ti] + ThetaI[n])  # Calculation of F
        #FV[Ti, n] = CV[n] * np.cos(n * 2 * pi * f * t[Ti] + ThetaV[n])
    RMSI[n] = np.sqrt(sum(FI[:-1, n] ** 2) / ns)  # RMS of each harmonic / Current
    HfI[n] = 100 * RMSI[n] / RMSI[1]
    HrmsI[n] = 100 * RMSI[n] / rmsI
    # RMSV[n] = np.sqrt(sum(FV[:-1, n] ** 2) / ns)  # RMS of each harmonic / Voltage
    # HfV[n] = 100 * RMSV[n] / RMSV[1]
    # HrmsV[n] = 100 * RMSV[n] / rmsV
    # print('%d-%d\n' % (n,Ti))

if (rmsI >= RMSI[1]):
    THDI = 100 * np.sqrt(((rmsI / RMSI[1]) ** 2) - 1)  # Calculation of THD ; current
else:
    THDI = 100 * (np.sqrt(sum((RMSI[2:41]) ** 2)) / RMSI[1])

dataHI = sum(FI, 1) + avgI

# if (rmsV >= RMSV[1]):
#     THDV = 100 * np.sqrt(((rmsV / RMSV[1]) ** 2) - 1)  # Calculation of THD ; voltage
# else:
#     THDV = 100 * (np.sqrt(sum((RMSV[2:41]) ** 2)) / RMSV[1])
#
# dataHV = sum(FV, 1) + avgV

THC = np.sqrt(sum(RMSI[2:41] ** 2))  # CHECK INDEX 40 OR 41!! Calculation of THC (Total Harmonic Current)

z = np.arange(14, 41)  # Calculation of PWHC (Partial Weighted Harmonic current)
H2 = RMSI[14:41] ** 2
PWHC = np.sqrt(sum(z * H2))

# Calculation of Phase Difference

PhaseDiff = (ThetaI[1] - ThetaV[1]) * 180 / pi
if (PhaseDiff > -0.01) & (PhaseDiff < 0.01):
    PhaseDiff = 0
if (PhaseDiff <= 180) & (PhaseDiff > 0):
    leadlag = 'leads'
    PhaseDiff_R = PhaseDiff
elif (PhaseDiff < 0) & (PhaseDiff > -180):
    leadlag = 'lags'
    PhaseDiff_R = abs(PhaseDiff)
elif (PhaseDiff > 180) & (PhaseDiff < 360):
    leadlag = 'lags'
    PhaseDiff_R = 360 - PhaseDiff
elif (PhaseDiff > -360) & (PhaseDiff < -180):
    leadlag = 'leads'
    PhaseDiff_R = 360 + PhaseDiff
elif (PhaseDiff == 0):
    leadlag = 'is in phase with'
    PhaseDiff_R = PhaseDiff

PhaseDiff5 = (ThetaI[5] - ThetaV[1]) * 180 / pi
if (PhaseDiff5 > -0.01) & (PhaseDiff5 < 0.01):
    PhaseDiff5 = 0
if (PhaseDiff5 <= 180) & (PhaseDiff5 > 0):
    leadlag5 = 'leads'
    PhaseDiff5_R = PhaseDiff5
elif (PhaseDiff5 > 180) & (PhaseDiff5 < 360):
    leadlag5 = 'lags'
    PhaseDiff5_R = 360 - PhaseDiff5
elif (PhaseDiff5 > -180) & (PhaseDiff5 < 0):
    leadlag5 = 'lags'
    PhaseDiff5_R = (-1) * PhaseDiff5
elif (PhaseDiff5 > -360) & (PhaseDiff5 < -180):
    leadlag5 = 'leads'
    PhaseDiff5_R = 360 + PhaseDiff5
elif (PhaseDiff5 == 0):
    leadlag5 = 'is in phase with'
    PhaseDiff5_R = PhaseDiff5

# Calculation of values

Pt = sum((dataI[:ns] * dataV[:ns]) / ns)  # Active Power

St = rmsI * rmsV  # Apparent Power

Q = RMSI * RMSV * np.sin(ThetaI - ThetaV)
Qt = sum(Q)  # Reactive Power

D = np.sqrt((St ** 2) - (Pt ** 2) - (Qt ** 2))  # Distortion Power

Pv = [St, Pt, Qt, D]  # Power Vector

distF = RMSI[1] / rmsI  # Distortion Factor

dispF = np.cos(ThetaI[1] - ThetaV[1])  # Displacement Factor

PF = distF * dispF  # Power Factor

# Print results to screen

print('The Voltage THD is %0.2f%%.' % (THDV))
print('The Current THD is %0.2f%%.' % (THDI))
print('The THC is %0.2f A.' % (THC))
print('The PWHC is %0.2f A.' % (PWHC))
print('The RMS value of the voltage is %0.2f V.' % (rmsV))
print('The RMS value of the current is %0.2f A.' % (rmsI))
if PhaseDiff == 0:
    print('The Fundamental Current' + leadlag + 'the Fundamental Voltage.')
elif PhaseDiff != 0:
    print('The Fundamental Current ' + leadlag + ' the Fundamental Voltage by %0.2f degrees.' % (PhaseDiff_R))
if PhaseDiff5 == 0:
    print('The 5th Harmonic of the Current' + leadlagR + 'the fundamental of the Voltage.')
elif PhaseDiff5 != 0:
    print('The 5th Harmonic of the Current ' + leadlag5 + ' the fundamental of the Voltage by %0.2f degrees.' % (
        PhaseDiff5_R))

input('Press Enter to continue')

# Print results to Excel file


book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Current")

sheet1.write(1, 0, "Irms [A]")
sheet1.write(2, 0, "I1 [A]")  # Fundamental
sheet1.write(3, 0, "THDi [%]")
sheet1.write(4, 0, "PWHC/I1 [%]")

sheet1.write(1, 1, rmsI)
sheet1.write(2, 1, RMSI[1])
sheet1.write(3, 1, THDI)
sheet1.write(4, 1, 100 * PWHC / RMSI[1])

sheet1.write(1, 2, "RMS Current")
sheet1.write(2, 2, "RMS Fundamental Current")
sheet1.write(3, 2, "Total Harmonic Current Distortion")
sheet1.write(4, 2, "Partial Weighted Harmonic Current")

sheet1.write(6, 0, "Harmonic content", easyxf('font:bold 1'))
sheet1.write(6, 1, "[%]", easyxf('font:bold 1'))
sheet1.write(6, 2, "[A rms]", easyxf('font:bold 1'))

index = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13'
    , 'I14', 'I15', 'I16', 'I17', 'I18', 'I19', 'I20', 'I21', 'I22', 'I23', 'I24', 'I25'
    , 'I26', 'I27', 'I28', 'I29', 'I30', 'I31', 'I32', 'I33', 'I34', 'I35', 'I36', 'I37', 'I38'
    , 'I39', 'I40']

i = 6

for n in index:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 0, n)
    else:
        sheet1.write(i, 0, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

i = 6

for n in HfI[1:41]:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 1, n)
    else:
        sheet1.write(i, 1, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

i = 6

for n in RMSI[1:41]:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 2, n)
    else:
        sheet1.write(i, 2, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

##

sheet1 = book.add_sheet("Voltage")

sheet1.write(1, 0, "Vrms [V]")
sheet1.write(2, 0, "V1 [V]")  # Fundamental
sheet1.write(3, 0, "THDv [%]")

sheet1.write(1, 1, rmsV)
sheet1.write(2, 1, RMSV[1])
sheet1.write(3, 1, THDV)

sheet1.write(1, 2, "RMS Voltage")
sheet1.write(2, 2, "RMS Fundamental Voltage")
sheet1.write(3, 2, "Total Harmonic Voltage Distortion")

sheet1.write(6, 0, "Harmonic content", easyxf('font:bold 1'))
sheet1.write(6, 1, "[%]", easyxf('font:bold 1'))
sheet1.write(6, 2, "[V rms]", easyxf('font:bold 1'))

index = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13'
    , 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25'
    , 'V26', 'V27', 'V28', 'V29', 'V30', 'V31', 'V32', 'V33', 'V34', 'V35', 'V36', 'V37', 'V38'
    , 'V39', 'V40']

i = 6

for n in index:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 0, n)
    else:
        sheet1.write(i, 0, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

i = 6

for n in HfV[1:41]:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 1, n)
    else:
        sheet1.write(i, 1, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

i = 6

for n in RMSV[1:41]:
    i = i + 1
    if i % 2 == 0:
        sheet1.write(i, 2, n)
    else:
        sheet1.write(i, 2, n, easyxf('pattern: pattern solid_pattern, fore_colour aqua'))

book.save("Harm_Data.xls")

# Plot figures 

plt.figure(1)
plt.subplot(211)
plt.plot(1e3 * l, dataV[:ns], label='Measured Data')
plt.plot(1e3 * l, dataHV[:ns], 'r', linestyle='--', label='Calculated Data')
plt.plot(1e3 * l, FV[:-1, 1], 'g')
plt.plot(1e3 * l, FV[:-1, 3], 'g')
plt.plot(1e3 * l, FV[:-1, 5], 'g')
plt.plot(1e3 * l, FV[:-1, 7], 'g')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [V]')
plt.grid(which='both', axis='both', color='black', linestyle='--')
legend = plt.legend(loc=0, shadow=True, fontsize='small')

plt.subplot(212)
plt.plot(1e3 * l, dataI[:ns], label='Measured Data')
plt.plot(1e3 * l, dataHI[:ns], 'r', linestyle='--', label='Calculated Data')
plt.plot(1e3 * l, FI[:-1, 1], 'g')
plt.plot(1e3 * l, FI[:-1, 3], 'g')
plt.plot(1e3 * l, FI[:-1, 5], 'g')
plt.plot(1e3 * l, FI[:-1, 7], 'g')
plt.xlabel('Time [ms]')
plt.ylabel('Current [A]')
plt.grid(which='both', axis='both', color='black', linestyle='--')
legend = plt.legend(loc=0, shadow=True, fontsize='small')
plt.show()

## 5th Harmonic current and fundamental line-neutral voltage phase angle

# plt.figure(2)
# plt.plot(1e3*l,FV[:-1,1],'g',label='Fundamental of the L-N Voltage')
# plt.plot(1e3*l,FI[:-1,5],'r',label='5th Harmonic of the Current')
# plt.xlabel('Time [ms]')
# plt.ylabel('Fundamental of the L-N Voltage [V]')
# plt.title('5th Harmonic of Current and Fundamental of L-N Voltage')
# legend = plt.legend(loc=0, shadow=True, fontsize='small')
# plt.grid(which='both', axis='both', color='black', linestyle='--')
# plt.show()

plt.figure(2)
fig, ax1 = plt.subplots()
ax1.plot(1e3 * l, FV[:-1, 1], 'b')
ax1.set_xlabel('Time [ms]')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Fundamental of the L-N Voltage [V]')
ax2 = ax1.twinx()
ax2.plot(1e3 * l, FI[:-1, 5], 'r')
ax2.set_ylabel('5th Harmonic of the Current [A]')
ax1.grid(which='both', axis='both', color='black', linestyle='--')

plt.show()

## Harmonic Bar Plots

plt.figure(3)
plt.subplot(211)
ind = np.arange(1, 21, 1)
rects1 = plt.bar(ind, 100 * RMSV[1:21] / RMSV[1], width=1, align='center')
plt.title('Harmonic % with respect to Fundamental')
plt.ylabel('Voltage - Percentage')
plt.xlabel('Harmonic Number')
plt.xticks(ind)
plt.yticks(np.arange(0, 120, 10))

plt.subplot(212)
ind = np.arange(1, 21, 1)
rects2 = plt.bar(ind, 100 * RMSI[1:21] / RMSI[1], width=1, color='r', align='center')
plt.ylabel('Current - Percentage')
plt.xlabel('Harmonic Number')
plt.xticks(ind)
plt.yticks(np.arange(0, 120, 10))
plt.show()

input('Press Enter to continue')

# def autolabel(rects):
# attach some text labels
#    for rect in rects:
#        height = rect.get_height()
#        if height < 1:
#            plt.text(rect.get_x()+rect.get_width()/2, 1.05*height,'%d'%int(height),
#                ha='center', va='bottom',visible=0)
#        else:
#            plt.text(rect.get_x()+rect.get_width()/2, 1.05*height,'%d'%int(height),
#                ha='center', va='bottom',visible=1)

# autolabel(rects1)
# autolabel(rects2)
