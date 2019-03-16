from rest_framework import serializers
from motors.models import Motor, Bearing, Rotor, Stator, WarningLog, WeeklyRecord, Ufeature, CurrentSignalPack, \
    Vfeature, Wfeature, SymComponent, Uphase
from rest_framework.renderers import JSONRenderer


class BearingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bearing
        fields = ("name", "statu", 'memo')


class RotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rotor
        fields = ("name", "statu", 'memo')


class StatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stator
        fields = ("name", "statu", 'memo')


class MotorsSerializer(serializers.ModelSerializer):
    bearings = BearingsSerializer(many=True)
    rotors = RotorSerializer(many=True)
    stators = StatorSerializer(many=True)

    class Meta:
        model = Motor
        fields = ("name", 'sn', 'statu', 'memo', 'admin', 'bearings', 'rotors', 'stators')


class WarningMotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motor
        fields = ('name', 'statu')


class WarningLogSerializer(serializers.ModelSerializer):
    motor = WarningMotorSerializer()

    class Meta:
        model = WarningLog
        fields = "__all__"


class WeeklyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyRecord
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ufeature
        fields = ('thd',)


class PSFserializer(serializers.ModelSerializer):
    psf = serializers.SerializerMethodField()

    def get_psf(self, obj):
        psf = float(obj.estimated_parameter.replace('[', '').replace(']', '').replace('  ', ' ').strip().split(' ')[1])
        # Considering change the filed used to store estimated sin parameter, above line parses unnaturally.
        return psf

    class Meta:
        model = Uphase
        fields = ('psf',)


class MotorTrendSerializer(serializers.ModelSerializer):
    trend = serializers.SerializerMethodField()

    def get_trend(self, obj):
        all_features = Ufeature.objects.filter(signal_pack__motor_id=obj.id)[:100]
        trend_serializer = FeatureSerializer(all_features, many=True, context={'request': self.context['request']})
        trend_list = [item['thd'] for item in trend_serializer.data]

        all_packs = CurrentSignalPack.objects.filter(motor_id=obj.id)[:100]
        time_list = [pack.time.strftime('%Y-%m-%d') for pack in all_packs]
        return {'trend': trend_list,
                'time': time_list}

    class Meta:
        model = Motor
        fields = ('name', 'statu', 'trend')


class DashBoardRadarFeatureSerializer(serializers.ModelSerializer):
    rmsfeatures = serializers.SerializerMethodField()
    symfeatures = serializers.SerializerMethodField()
    psf = serializers.SerializerMethodField()

    def get_rmsfeatures(self, obj):
        import time
        start = time.time()
        return {'urms': Motor.objects.get(id=obj.id).packs.last().ufeature.rms,
                'vrms': Motor.objects.get(id=obj.id).packs.last().vfeature.rms,
                'wrms': Motor.objects.get(id=obj.id).packs.last().wfeature.rms}
        end = time.time()
        print(end - start)

    def get_symfeatures(self, obj):
        return {
            'ns': Motor.objects.get(id=obj.id).packs.last().symcomponent.n_sequence_rms,
            'ps': Motor.objects.get(id=obj.id).packs.last().symcomponent.n_sequence_rms,
        }

    def get_psf(self, obj):
        phase_object = Uphase.objects.filter(signal_pack__motor_id=obj.id).last()
        trend_serializer = PSFserializer(phase_object, context={'request': self.context['request']})
        return trend_serializer.data

    class Meta:
        model = Motor
        fields = ('name', 'rmsfeatures', 'symfeatures', 'psf')
