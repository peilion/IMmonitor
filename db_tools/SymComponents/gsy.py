import numpy as np
import db_tools.SymComponents.gsyTransforms as trf
import matplotlib.pyplot as plt
from scipy import optimize

SAMPLING_RATE = 20480
TIMEEND = 8192/20480
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
    p0 = [max(wave), freq[np.argmax(spec)], np.pi * freq[np.argmax(spec)]]  # Initial guess for the parameters
    # p0 = [max(data), 50, 0.7]
    Tx = np.linspace(0, size / sampling_rate, size)
    p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, wave))
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


# Load 3-phase data(fake), simply shifting the single phase signal.
from motors.models import CurrentSignalPack

pack = CurrentSignalPack.objects.last()
phaseA = np.fromstring(pack.vphase.signal)
phaseB = np.fromstring(pack.uphase.signal)
phaseC = np.fromstring(pack.wphase.signal)
Tx = np.linspace(0, TIMEEND, SAMPLE_NUMBER)

# Illustrate the original waveform.
plt.plot(Tx, phaseA, "b-", Tx, phaseB, "r-", Tx, phaseC, "g-", )  # Plot of the data and the fit
plt.show()

# Estimate the parameters.
time = np.linspace(Tx.min(), Tx.max(), 8192)
pA = parameter_estimation(phaseA, 20480)
pB = parameter_estimation(phaseB, 20480)
pC = parameter_estimation(phaseC, 20480)

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
