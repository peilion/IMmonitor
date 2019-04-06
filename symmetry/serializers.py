from rest_framework import serializers
from motors.models import CurrentSignalPack, Ufeature, SymComponent
from real_time.serializers import PhaseSerializer, fftransform
import numpy as np
from scipy import signal

def dq0_transform(v_a, v_b, v_c):
    d = (np.sqrt(2 / 3) * v_a - (1 / (np.sqrt(6))) * v_b - (1 / (np.sqrt(6))) * v_c)
    q = ((1 / (np.sqrt(2))) * v_b - (1 / (np.sqrt(2))) * v_c)
    return d, q


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


def cal_symm(a, b, c):
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


def to_complex(r, x, real_offset=0, imag_offset=0):
    real = r * np.cos(x) + real_offset

    imag = r * np.sin(x) + imag_offset

    return (real + 1j * imag)


class PackSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        uphase = PhaseSerializer(obj.uphase, many=False, context={'request': self.context['request']}).data
        vphase = PhaseSerializer(obj.vphase, many=False, context={'request': self.context['request']}).data
        wphase = PhaseSerializer(obj.wphase, many=False, context={'request': self.context['request']}).data
        complex_list = []
        for item in [uphase, vphase, wphase]:
            complex_phase, _ = make_phase(item['amplitude'],
                                          2 * np.pi * item['frequency'],
                                          item['initial_phase'], samples=1024, end_time=1024 / 20480)
            # Append to the list
            complex_list.append(complex_phase)

        (phaseA_pos, phaseB_pos, phaseC_pos,
         phaseA_neg, phaseB_neg, phaseC_neg,
         phaseZero) = cal_symm(complex_list[1],
                               complex_list[0],
                               complex_list[2])

        return {
            'pAp_real': phaseA_pos.real, 'pAp_imag': phaseA_pos.imag,
            'pBp_real': phaseB_pos.real, 'pBp_imag': phaseB_pos.imag,
            'pCp_real': phaseC_pos.real, 'pCp_imag': phaseC_pos.imag,
            'pAn_real': phaseA_neg.real, 'pAn_imag': phaseA_neg.imag,
            'pBn_real': phaseB_neg.real, 'pBn_imag': phaseB_neg.imag,
            'pCn_real': phaseC_neg.real, 'pCn_imag': phaseC_neg.imag,
            'zero_real': phaseZero.real, 'zero_imag': phaseZero.imag,
        }

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"


class PackListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CurrentSignalPack
        fields = ('id', 'time', 'rpm')


class DQPackSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        phaseA = np.fromstring(obj.vphase.signal)
        phaseB = np.fromstring(obj.uphase.signal)
        phaseC = np.fromstring(obj.wphase.signal)
        d, q = dq0_transform(phaseA, phaseB, phaseC)

        return {
            'A': phaseA, 'B': phaseB, 'C': phaseC, 'd': d, 'q': q,
            'd_rms': np.sqrt(np.dot(d, d) / d.size),
            'q_rms': np.sqrt(np.dot(q, q) / d.size)
        }

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ufeature
        exclude = ('harmonics', 'fbrb', 'signal_pack')


class SymmetryFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymComponent
        exclude = ('signal_pack',)


class TrendSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def get_data(self, obj):
        tempDict = {}
        for item, phase in zip([obj.ufeature, obj.vfeature, obj.wfeature], ['u', 'v', 'w']):
            tempDict[phase + 'feature'] = FeatureSerializer(item, many=False,
                                                            context={'request': self.context['request']}).data
        tempDict['symfeature'] = SymmetryFeatureSerializer(obj.symcomponent, many=False,
                                                           context={'request': self.context['request']}).data
        return tempDict

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"


class HamonicsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def get_data(self, obj):
        tempDict = {}
        for feature, phase, signal in zip([obj.ufeature, obj.vfeature, obj.wfeature], ['u', 'v', 'w'],
                                          [obj.uphase, obj.vphase, obj.wphase]):
            tempDict[phase + 'harmonic'] = np.fromstring(feature.harmonics)
            tempDict[phase + 'fft'] = np.around(fftransform(np.fromstring(signal.signal)), decimals=3)
            tempDict[phase + 'thd'] = feature.thd
        return tempDict

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"


class EnvelopeSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def get_data(self, obj):
        tempDict = {}
        for phase_obj, phase in zip([obj.uphase, obj.vphase, obj.wphase], ['u', 'v', 'w']):
            raw_signal = signal.detrend(np.fromstring(phase_obj.signal))
            tempDict[phase + 'envelope'] = np.abs(signal.hilbert(raw_signal)[1024:1024 + 4096])
            tempDict[phase + 'fft'] = np.around(fftransform(signal.detrend(tempDict[phase + 'envelope'])), decimals=3)
            tempDict[phase + 'raw'] = raw_signal[1024:1024 + 4096]

        return tempDict

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"
