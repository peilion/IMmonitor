import numpy as np
from motors.models import Motor, CurrentSignalPack, Uphase, Ufeature
from rest_framework import serializers


def fftransform(Signal):
    # fft_size = int(Signal.shape[0])
    spec = np.fft.rfft(Signal)
    # freq = np.linspace(0, 10240 / 2, fft_size / 2 + 1)
    spec = np.abs(spec)
    return spec


class PackSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CurrentSignalPack
        fields = ('id', 'time', 'sampling_rate', 'rpm')


class PhaseSerializer(serializers.ModelSerializer):
    signal = serializers.SerializerMethodField()
    spec = serializers.SerializerMethodField()

    def get_signal(self, obj):
        return np.around(np.fromstring(obj.signal), decimals=3)

    def get_spec(self, obj):
        return np.around(fftransform(self.get_signal(obj)), decimals=3)

    class Meta:
        model = Uphase
        fields = ('signal', 'frequency', 'amplitude', 'initial_phase', 'spec',)


class FeatureSerilizer(serializers.ModelSerializer):
    harmonics = serializers.SerializerMethodField()
    fbrb = serializers.SerializerMethodField()

    def get_harmonics(self, obj):
        return np.fromstring(obj.harmonics)

    def get_fbrb(self, obj):
        return np.fromstring(obj.fbrb)

    class Meta:
        model = Ufeature
        fields = '__all__'


class RealTimeMotorSerializer(serializers.ModelSerializer):
    threephase = serializers.SerializerMethodField()
    pack = serializers.SerializerMethodField()
    feature = serializers.SerializerMethodField()

    def get_feature(self, obj):
        pack = obj.packs.last()
        ufeature = FeatureSerilizer(pack.ufeature, many=False, context={'request': self.context['request']}).data
        vfeature = FeatureSerilizer(pack.vfeature, many=False, context={'request': self.context['request']}).data
        wfeature = FeatureSerilizer(pack.wfeature, many=False, context={'request': self.context['request']}).data

        return {
            'ufeature': ufeature,
            'vfeature': vfeature,
            'wfeature': wfeature,
        }

    def get_pack(self, obj):
        pack = PackSerializer(obj.packs.last(), many=False, context={'request': self.context['request']}).data,
        return pack[0]

    def get_threephase(self, obj):
        pack = obj.packs.last()
        uphase = PhaseSerializer(pack.uphase, many=False, context={'request': self.context['request']}).data
        vphase = PhaseSerializer(pack.vphase, many=False, context={'request': self.context['request']}).data
        wphase = PhaseSerializer(pack.wphase, many=False, context={'request': self.context['request']}).data

        return {
            'uphase': uphase,
            'vphase': vphase,
            'wphase': wphase,
        }

    class Meta:
        model = Motor
        fields = ('name', 'threephase', 'pack', 'feature')
