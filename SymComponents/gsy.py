import numpy as np
import gsyTransforms as trf
import matplotlib.pyplot as plt
from scipy import io as sio
from scipy import optimize

TIMEEND = 0.1
SAMPLING_RATE = 20000
SAMPLE_NUMBER = int(TIMEEND * SAMPLING_RATE)


def cal_samples(phaseAOmega, phaseBOmega, phaseCOmega):
    '''
    Calculate the number of samples needed.
    '''
    max_omega = max(abs(phaseAOmega),
                    abs(phaseBOmega),
                    abs(phaseCOmega))
    max_freq = max_omega / (2 * np.pi)
    samples = (max_freq ** 2) * 6 * TIMEEND
    return samples


def make_phase(mag, omega, phi):
    '''
    Create the phase signal in complex form.
    '''

    samples = cal_samples(2 * np.pi * pA[1], 2 * np.pi * pB[1], 2 * np.pi * pC[1])

    array_time = np.linspace(0, TIMEEND, samples)

    x = omega * array_time + phi

    return trf.to_complex(mag, x), array_time


def parameter_estimation(wave, sampling_rate):
    fitfunc = lambda p, x: p[0] * np.sin(2 * np.pi * p[1] * x + p[2])  # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function
    size = int(wave.shape[0])
    spec = np.fft.rfft(wave)
    freq = np.linspace(0, sampling_rate / 2, size / 2 + 1)
    spec = np.abs(spec)
    p0 = [max(data), freq[np.argmax(spec)], np.pi * freq[np.argmax(spec)]]  # Initial guess for the parameters
    # p0 = [max(data), 50, 0.7]
    Tx = np.linspace(0, size / sampling_rate, size)
    p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, wave))
    return p1


# Load 3-phase data(fake), simply shifting the single phase signal.
load_fn = 'Health_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data'][:, 0]
phaseA = data[500000:500000 + SAMPLE_NUMBER]
phaseB = data[500000 - 133:500000 + SAMPLE_NUMBER - 133]
phaseC = data[500000 + 133:500000 + SAMPLE_NUMBER + 133]
Tx = np.linspace(0, TIMEEND, SAMPLE_NUMBER)

# Illustrate the original waveform.
plt.plot(Tx, phaseA, "b-", Tx, phaseB, "r-", Tx, phaseC, "g-", )  # Plot of the data and the fit
plt.show()

# Estimate the parameters.
time = np.linspace(Tx.min(), Tx.max(), 2000)
pA = parameter_estimation(phaseA, 20000)
pB = parameter_estimation(phaseB, 20000)
pC = parameter_estimation(phaseC, 20000)

# Illustrate the fitted curve.
fitfunc = lambda p, x: p[0] * np.sin(2 * np.pi * p[1] * x + p[2])  # Target function
plt.plot(time, fitfunc(pA, time), "b-", time, fitfunc(pB, time), "r-", time, fitfunc(pC, time),
         "g-")  # Plot of the data and the fit
plt.show()

# Construct complex signal from estimated signal.
phaseAdata, time_samples = make_phase(pA[0] * 1.1,
                                      2 * np.pi * pA[1],
                                      pA[2])
phaseBdata, _ = make_phase(pB[0],
                           2 * np.pi * pB[1],
                           pB[2])
phaseCdata, _ = make_phase(pC[0],
                           2 * np.pi * pC[1],
                           pC[2])

plt.plot(time_samples, phaseAdata, "b-", time_samples, phaseBdata, "r-", time_samples, phaseCdata, "g-")
plt.show()

# Calculate the Symmetrical components
(phaseA_pos, phaseB_pos, phaseC_pos,
 phaseA_neg, phaseB_neg, phaseC_neg,
 phaseZero) = trf.cal_symm(phaseAdata,
                           phaseBdata,
                           phaseCdata)

plt.plot(time_samples, phaseA_pos, "b-", time_samples, phaseB_pos, "r-", time_samples, phaseC_pos,
         "g-")  # Plot of the data and the fit
plt.show()

plt.plot(time_samples, phaseA_neg, "b-", time_samples, phaseB_neg, "r-", time_samples, phaseC_neg,
         "g-")  # Plot of the data and the fit
plt.ylim([-0.3, 0.3])
plt.show()
