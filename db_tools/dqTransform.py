from motors.models import CurrentSignalPack
import numpy as np
import matplotlib.pyplot as plt
pack = CurrentSignalPack.objects.last()

phaseA = np.fromstring(pack.vphase.signal)
phaseB = np.fromstring(pack.uphase.signal)
phaseC = np.fromstring(pack.wphase.signal)

plt.plot( phaseA, "b-", phaseB, "r-", phaseC, "g-", )  # Plot of the data and the fit
plt.show()

a = -1/2+1j*np.sqrt(3)/2
a2 = -1/2-1j*np.sqrt(3)/2

In = 1/3*(phaseA+a2*phaseB+a*phaseC)
Ip = 1/3*(phaseA+a*phaseB+a2*phaseC)

plt.plot( In, "b-")  # Plot of the data and the fit
plt.show()
plt.plot(Ip, "r-")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
# User configurable
freq = 1/60
end_time = 180
v_peak = 220
step_size = 0.01
# Find the three-phase voltages
v1 = []
v2 = []
v3 = []
thetas = 2 * np.pi * freq * np.arange(0,end_time,step_size)
for ii, t in enumerate(thetas):
    v1.append(v_peak * np.sin(t))
    v2.append(v_peak * np.sin(t - (2/3+1/10)*np.pi))
    v3.append(v_peak * np.sin(t - (4/3)*np.pi))
v1, v2, v3 = np.array(v1), np.array(v2), np.array(v3)
# Plot the results
plt.plot(v1, label="V1")
plt.plot(v2, label="V2")
plt.plot(v3, label="V3")
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.legend(ncol=3)
plt.show()
def dq0_transform(v_a, v_b, v_c):
    d=(np.sqrt(2/3)*v_a-(1/(np.sqrt(6)))*v_b-(1/(np.sqrt(6)))*v_c)
    q=((1/(np.sqrt(2)))*v_b-(1/(np.sqrt(2)))*v_c)
    return d, q

# Calculate and plot the results
d, q = dq0_transform(phaseA, phaseB,phaseC)
d, q = dq0_transform(v1, v2,v3)

plt.figure()
plt.plot(d, q)
plt.xlabel('D Phase')
plt.ylabel('Q Phase')
plt.show()
