from motors.models import CurrentSignalPack, Ufeature, Vfeature, Wfeature, SymComponent, Uprocessed, Vprocessed, Uphase, \
    Vphase, Wphase, Wprocessed
import numpy as np
from scipy import signal, fftpack, optimize

dataset = CurrentSignalPack.objects.all()
import matplotlib.pyplot as plt
import time


def cal_samples(phaseAOmega, phaseBOmega, phaseCOmega, end_time):
    '''
    Calculate the number of samples needed.
    '''
    max_omega = max(abs(phaseAOmega),
                    abs(phaseBOmega),
                    abs(phaseCOmega))
    max_freq = max_omega / (2 * np.pi)
    samples = (max_freq ** 2) * 6 * end_time
    return samples


def make_phase(mag, omega, phi, samples, end_time):
    '''
    Create the phase signal in complex form.
    '''

    array_time = np.linspace(0, end_time, samples)

    x = omega * array_time + phi

    return to_complex(mag, x), array_time


def parameter_estimation(wave, sampling_rate, initailization):
    fitfunc = lambda p, x: p[0] * np.sin(2 * np.pi * p[1] * x + p[2])  # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function
    size = int(wave.shape[0])
    Tx = np.linspace(0, size / sampling_rate, size)
    p1, success = optimize.leastsq(errfunc, initailization[:], args=(Tx, wave))
    return p1


def cal_symm(a, b, c):
    """
    .. _cal_symm :
    Calculates the 3-phase symmetrical components (Fortescue).
    Accepts complex form of three-phase inputs. Returns the Positive sequence,
    the Negative sequence and the Zero sequence.
    .. math ::
        A = e^{j \\frac{2}{3} \pi} = \\angle 120^{\circ}

    Commonly, the lowercase of :math:`A`, :math:`\\alpha`, is used.
    To avoid confusion with :math:`a` (/eɪ/), the uppercase, :math:`A`, is used here instead.
    .. math ::
        \left[\\begin{matrix}
        a_{+} \\\\ b_{+} \\\\ c_{+}
        \end{matrix}\\right]
        &= \\frac{1}{3}
        \left[\\begin{matrix}
        1 & A & A^2
        \\\\ A^2 & 1 & A
        \\\\ A & A^2 & 1
        \end{matrix}\\right]
        \left[\\begin{matrix}
        a \\\\ b \\\\ c
        \end{matrix}\\right]
        \\\\
        \left[\\begin{matrix}
        a_{-} \\\\ b_{-} \\\\ c_{-}
        \end{matrix}\\right]
        &= \\frac{1}{3}
        \left[\\begin{matrix}
        1 & A^2 & A
        \\\\ A & 1 & A^2
        \\\\ A^2 & A & 1
        \end{matrix}\\right]
        \left[\\begin{matrix}
        a \\\\ b \\\\ c
        \end{matrix}\\right]

        \\\\
        \left[\\begin{matrix}
        a_{Zero} \\\\ b_{Zero} \\\\ c_{Zero}
        \end{matrix}\\right]
        = \\frac{1}{3}
        \left[\\begin{matrix}
        1 & 1 & 1
        \\\\ 1 & 1 & 1
        \\\\ 1 & 1 & 1
        \end{matrix}\\right]
        \left[\\begin{matrix}
        a \\\\ b \\\\ c
        \end{matrix}\\right]
    ===================== ============================================================
    where:
    ===================== ============================================================
    :math:`A`               is the :math:`120^{\circ}` shifter;
    :math:`a`               is the Phase-A input;
    :math:`b`               is the Phase-B input;
    :math:`c`               is the Phase-C input;
    :math:`a_+`             is the positive sequence of Phase-A input;
    :math:`b_+`             is the positive sequence of Phase-B input;
    :math:`c_+`             is the positive sequence of Phase-C input;
    :math:`a_-`             is the negative sequence of Phase-A input;
    :math:`b_-`             is the negative sequence of Phase-B input;
    :math:`c_-`             is the negative sequence of Phase-C input;
    :math:`a_{Zero}`        is the zero sequence of Phase-A input;
    :math:`b_{Zero}`        is the zero sequence of Phase-B input;
    :math:`c_{Zero}`        is the zero sequence of Phase-C input.
    ===================== ============================================================
    Parameters
    ----------
    a : complex or a list of complex
        Phase-A inputs
    b : complex or a list of complex
        Phase-B inputs
    c : complex or a list of complex
        Phase-C inputs
    Returns
    -------
    a_pos : complex or a list of complex
        Phase-A Positive sequence.
    b_pos : complex or a list of complex
        Phase-B Positive sequence.
    c_pos : complex or a list of complex
        Phase-C Positive sequence.
    a_neg : complex or a list of complex
        Phase-A Negative sequence.
    b_neg : complex or a list of complex
        Phase-B Negative sequence.
    c_neg : complex or a list of complex
        Phase-C Negative sequence.
    Zero : complex or a list of complex
        Ther Zero sequence. Since all zero sequence components are
        the same, only one is returned.


    Examples
    --------

    .. code :: python
        import gsyTransforms as trf
        (phaseA_pos, phaseB_pos,
         phaseC_pos, phaseA_neg,
         phaseB_neg, phaseC_neg,
         phaseZero)              = trf.cal_symm(phaseAdata,
                                                phaseBdata,
                                                phaseCdata)
    """

    # 120 degree rotator
    ALPHA = np.exp(1j * 2 / 3 * np.pi)

    # Positive sequence
    a_pos = 1 / 3 * (a + b * ALPHA + c * (ALPHA ** 2))

    b_pos = 1 / 3 * (a * (ALPHA ** 2) + b + c * ALPHA)

    c_pos = 1 / 3 * (a * ALPHA + b * (ALPHA ** 2) + c)

    # Negative sequence
    a_neg = 1 / 3 * (a + b * (ALPHA ** 2) + c * ALPHA)

    b_neg = 1 / 3 * (a * ALPHA + b + c * (ALPHA ** 2))

    c_neg = 1 / 3 * (a * (ALPHA ** 2) + b * ALPHA + c)

    # zero sequence
    zero = 1 / 3 * (a + b + c)

    return a_pos, b_pos, c_pos, a_neg, b_neg, c_neg, zero


def fftransform(Signal):
    # fft_size = int(Signal.shape[0])
    spec = np.fft.rfft(Signal)
    # freq = np.linspace(0, 10240 / 2, fft_size / 2 + 1)
    spec = np.abs(spec)
    return spec


def to_complex(r, x, real_offset=0, imag_offset=0):
    real = r * np.cos(x) + real_offset

    imag = r * np.sin(x) + imag_offset

    return (real + 1j * imag)


for pack in dataset:
    # st = time.time()
    u = np.fromstring(pack.uphase.signal)
    v = np.fromstring(pack.vphase.signal)
    w = np.fromstring(pack.wphase.signal)

    RATE = pack.sampling_rate
    LENGTH = u.shape[0]
    FREQ_INTERVAL = RATE / 2 / (LENGTH / 2)
    spectrum_list = []
    PSF_list = []
    envelope_list = []
    hspectrum_list = []
    complex_list = []
    max_list = []
    harmonics_list = []
    THD_list = []
    rms_list = []
    min_list = []
    for phase in [u, v, w]:
        # FFt
        phase = signal.detrend(phase, type='constant')
        phase_fft = fftransform(phase)
        phase_fft_axis = np.linspace(0, RATE / 2, len(phase) / 2 + 1)

        # Power supply frequency
        PSF = phase_fft_axis[np.argmax(phase_fft)]

        harmonics_index = [i * PSF / FREQ_INTERVAL for i in range(2, 20)]
        total = 0
        harmonics = []
        fundamental = phase_fft[int(PSF / FREQ_INTERVAL)]
        for hm in harmonics_index:
            nth_harmonic = phase_fft[int(hm)] / fundamental
            total = total + nth_harmonic ** 2
            harmonics.append(nth_harmonic)
        # total = np.sqrt(total)
        THD = np.sqrt(total)

        # Hilbert transform
        Shiftted = np.abs(signal.hilbert(phase))
        phase_envelope = signal.detrend(Shiftted[1024:1024 + 4096])
        # Hilebert spectrum
        phase_envelope_fft = fftransform(phase_envelope)
        phase_envelope_fft_axis = np.linspace(0, RATE / 2, len(phase_envelope) / 2 + 1)

        # RMS
        rms = np.sqrt(np.dot(phase, phase) / phase.size)

        # Maximum and minimum
        maximum = np.max(phase)
        minimum = np.min(phase)
        spectrum_list.append(phase_fft)
        envelope_list.append(phase_envelope)
        hspectrum_list.append(fftransform(phase_envelope_fft))
        PSF_list.append(PSF)
        max_list.append(maximum)
        harmonics_list.append(harmonics)
        THD_list.append(THD)
        rms_list.append(rms)
        min_list.append(minimum)
    i = 0
    p = []
    for phase in [u, v, w]:
        # Estimate parameters
        p0 = [max_list[i], PSF_list[i], np.pi * PSF_list[i]]  # Initial guess for the parameters
        p1 = parameter_estimation(phase, RATE, initailization=p0)
        p.append(p1)
        i = i + 1
        # Calculate complex data

    samples = cal_samples(2 * np.pi * p[0][1], 2 * np.pi * p[1][1], 2 * np.pi * p[2][1], end_time=LENGTH / RATE)

    i = 0
    for phase in [u, v, w]:
        complex_phase, _ = make_phase(p[i][0],
                                      2 * np.pi * p[i][1],
                                      p[i][2], samples=int(samples), end_time=LENGTH / RATE)
        # Append to the list
        complex_list.append(complex_phase)
        i = i + 1

    (phaseA_pos, phaseB_pos, phaseC_pos,
     phaseA_neg, phaseB_neg, phaseC_neg,
     phaseZero) = cal_symm(complex_list[0],
                           complex_list[1],
                           complex_list[2])


    # end = time.time()
    # print(end-st)

    def create_feature(feature, index):
        feature.objects.create(signal_pack=pack,
                               rms=rms_list[index],
                               thd=THD_list[index],
                               harmonics_list=str(harmonics[index]),
                               max_current=max_list[index],
                               min_current=min_list[index])


    create_feature(Ufeature, index=0)
    create_feature(Vfeature, index=1)
    create_feature(Wfeature, index=2)


    def update_phase(phase, index):
        phase.objects.get(signal_pack=pack).update(complex_signal=complex_list[index].tostring())


    update_phase(Uphase, index=0)
    update_phase(Vphase, index=1)
    update_phase(Wphase, index=2)


    def create_processed(processed, index):
        processed.objects.create(signal_pakc=pack,
                                 spec=spectrum_list[index],
                                 env=envelope_list[index],
                                 env_spec=hspectrum_list[index], )


    create_processed(Uprocessed, index=0)
    create_processed(Vprocessed, index=1)
    create_processed(Wprocessed, index=2)

    n_rms = np.sqrt(np.dot(phaseA_neg, phaseA_neg) / phase.size)
    p_rms = np.sqrt(np.dot(phaseA_pos, phaseA_pos) / phase.size)
    SymComponent.objects.create(signal_pack=pack,
                                nagative_sequence=phaseA_neg.tostring(),
                                positive_sequence=phaseA_pos.tostring(),
                                zero_sequence=phaseZero,
                                n_sequence_rms=n_rms,
                                p_sequence_rms=p_rms,
                                z_sequence_rms=np.sqrt(np.dot(phaseZero, phaseZero) / phase.size),
                                imbalance=n_rms / p_rms,
                                )

    # F50L5 = [1325, 1475, 1625, 1775]
    # F40L5 = [725, 875, 1025, 1175]
    # F30L5 = [125, 275, 425, 675]
    #
    # temp = F30L5
    # spec1, freq = pack_process(CurrentSignalPack.objects.get(id=temp[0]))  # 蓝
    # spec2, _ = pack_process(CurrentSignalPack.objects.get(id=temp[1]))  # 橙
    # spec3, _ = pack_process(CurrentSignalPack.objects.get(id=temp[2]))  # 绿
    # spec4, _ = pack_process(CurrentSignalPack.objects.get(id=temp[3]))  # 红
    #
    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].plot(freq, spec1)
    # axs[0, 0].set_xlim(0, 100)
    # axs[0, 0].set_ylim(0, 12.5)
    # axs[0, 0].set_ylabel('BRB')
    #
    # axs[0, 1].plot(freq, spec2)
    # axs[0, 1].set_xlim(0, 100)
    # axs[0, 1].set_ylabel('BRM')
    # axs[0, 1].set_ylim(0, 12.5)
    #
    # axs[1, 0].plot(freq, spec3)
    # axs[1, 0].set_xlim(0, 100)
    # axs[1, 0].set_ylabel('HEA')
    # axs[1, 0].set_ylim(0, 12.5)
    #
    # axs[1, 1].plot(freq, spec4)
    # axs[1, 1].set_xlim(0, 100)
    # axs[1, 1].set_ylabel('RMAM')
    # axs[1, 1].set_ylim(0, 12.5)
    #
    # fig.tight_layout()
    # plt.show()
