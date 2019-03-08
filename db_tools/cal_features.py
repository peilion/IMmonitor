from motors.models import CurrentSignalPack
import numpy as np
from scipy import signal, fftpack

dataset = CurrentSignalPack.objects.all()


def fftransform(Signal):
    # fft_size = int(Signal.shape[0])
    spec = np.fft.rfft(Signal)
    # freq = np.linspace(0, 10240 / 2, fft_size / 2 + 1)
    spec = np.abs(spec)
    return spec


for pack in dataset:
    u = np.fromstring(pack.uphase.signal)
    v = np.fromstring(pack.vphase.signal)
    w = np.fromstring(pack.wphase.signal)
    RATE = pack.sampling_rate

    spectrum_list = []
    envelope_list = []
    hspectrum_list = []
    for phase in [u, v, w]:
        # FFt
        phase = signal.detrend(phase, type='constant')
        phase_fft = fftransform(phase)
        phase_fft_axis = np.linspace(0, RATE / 2, len(phase) / 2 + 1)

        # Power supply frequency
        PSF = phase_fft_axis[np.argmax(phase_fft)]

        # Hilbert transform
        Shiftted = np.abs(signal.hilbert(phase))
        phase_envelope = signal.detrend(Shiftted[1024:1024+4096], type='constant')

        # Hilebert spectrum
        phase_envelope_fft = fftransform(phase_envelope)
        phase_envelope_fft_axis = np.linspace(0, RATE / 2, len(phase_envelope) / 2 + 1)

        # RMS
        rms = np.sqrt(np.dot(phase, phase) / phase.size)

        # Maximum and minimum
        maximum = np.max(phase)
        minimum = np.min(phase)

        # Append to the list
        spectrum_list.append(phase_fft)
        envelope_list.append(phase_envelope)
        hspectrum_list.append(fftransform(phase_envelope_fft))
