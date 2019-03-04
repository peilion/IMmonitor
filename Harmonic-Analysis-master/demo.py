import numpy as np
import scipy.io as sio


def cal_harmonic(csv):
    sp = np.fft.fft(csv)
    spec = np.abs(sp)
    harmonics = [i * 10 for i in range(2, 40)]
    total = 0
    for hm in harmonics:
        total = total + spec[hm] * spec[hm]

    #total = np.sqrt(total)
    THD = total / (spec[10]*spec[10])
    return THD


load_fn = 'BRB_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data']
data = data[:, 0]
csv = data[500000:504000]
THD_BRB = cal_harmonic(csv)


load_fn = 'Health_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data']
data = data[:, 0]
csv = data[500000:504000]
THD_HEALTH = cal_harmonic(csv)

load_fn = 'BRM_50Hz_Load_0.mat'
load_data = sio.loadmat(load_fn)
data = load_data['data']
data = data[:, 0]
csv = data[500000:504000]
THD_BRM = cal_harmonic(csv)


