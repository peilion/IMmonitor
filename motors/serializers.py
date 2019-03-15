from rest_framework import serializers
from motors.models import Motor, Bearing, Rotor, Stator, WarningLog, WeeklyRecord, Ufeature, CurrentSignalPack
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
