import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import io as sio


def parameter_estimation(wave, sampling_rate):
    fitfunc = lambda p, x: p[0] * np.sin(2 * np.pi * p[1] * x + p[2])  # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function
    size = int(wave.shape[0])
    # spec = np.fft.rfft(wave)
    # freq = np.linspace(0, sampling_rate / 2, size / 2 + 1)
    # spec = np.abs(spec)
    #p0 = [max(data), freq[np.argmax(spec)], 0.1]  # Initial guess for the parameters
    p0 = [max(data), 50, 0.7]
    Tx = np.linspace(0, size / sampling_rate, size)

    p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, wave))
    return p1


load_fn = 'Health_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data']

data = data[:, 0]
phaseA = data[500000:502000]
phaseB = data[500000 - 133:502000 - 133]
phaseC = data[500000 + 133:502000 + 133]

num_points = 2000
Tx = np.linspace(0, 0.1, num_points)

plt.plot(Tx, phaseA, "b-", Tx, phaseB, "r-", Tx, phaseC, "g-", )  # Plot of the data and the fit
plt.show()

# Fit the first set
time = np.linspace(Tx.min(), Tx.max(), 2000)

import time
start=time.time()
pA = parameter_estimation(phaseA, 20000)
pB = parameter_estimation(phaseB, 20000)
pC = parameter_estimation(phaseC, 20000)
end = time.time()
consumption = end-start

fitfunc = lambda p, x: p[0] * np.sin(2 * np.pi * p[1] * x + p[2])  # Target function
plt.plot(time, fitfunc(pA, time), "b-", time, fitfunc(pB, time), "r-", time, fitfunc(pC, time), "g-") # Plot of the data and the fit
plt.show()