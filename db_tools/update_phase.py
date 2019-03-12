from motors.models import CurrentSignalPack, Ufeature, Vfeature, Wfeature, SymComponent, Uprocessed, Vprocessed, Uphase, \
    Vphase, Wphase, Wprocessed
import numpy as np
from scipy import signal, fftpack, optimize

dataset = CurrentSignalPack.objects.all()
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
        maximum = np.max(phase)
        max_list.append(maximum)
        PSF = phase_fft_axis[np.argmax(phase_fft)]

        PSF_list.append(PSF)

        # Power supply frequency
        PSF = phase_fft_axis[np.argmax(phase_fft)]
        # Maximum and minimum
    i = 0
    p = []
    for phase in [u, v, w]:
        # Estimate parameters
        p0 = [max_list[i], PSF_list[i], np.pi * PSF_list[i]]  # Initial guess for the parameters
        p1 = parameter_estimation(phase, RATE, initailization=p0)
        p.append(p1)
        i = i + 1
        # Calculate complex data

    def update_phase(phase, index):
        _t = phase.objects.get(signal_pack=pack)
        _t.estimated_parameter = str(p[index])
        _t.save()


    update_phase(Uphase, index=0)
    update_phase(Vphase, index=1)
    update_phase(Wphase, index=2)