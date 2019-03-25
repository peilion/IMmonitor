from rest_framework import serializers
from motors.models import Motor, Bearing, Rotor, Stator, WarningLog, WeeklyRecord, Ufeature, CurrentSignalPack, \
    Vfeature, Wfeature, SymComponent, Uphase
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
import itertools


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class BearingsSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    def get_admin(self, obj):
        return UserSeralizer(obj.motor.admin).data

    class Meta:
        model = Bearing
        fields = ('id', "name", 'health_indicator', "statu", 'lr_time', 'tags', 'memo', 'admin')


class RotorSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    class Meta:
        model = Rotor
        fields = ('id', "name", 'health_indicator', "statu", 'lr_time', 'tags', 'memo', 'admin')

    def get_admin(self, obj):
        return UserSeralizer(obj.motor.admin).data


class StatorSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    class Meta:
        model = Stator
        fields = ('id', "name", 'health_indicator', "statu", 'lr_time', 'tags', 'memo', 'admin')

    def get_admin(self, obj):
        return UserSeralizer(obj.motor.admin).data


class MotorsSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    admin = UserSeralizer()
    detail = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = [
            BearingsSerializer(obj.bearings.exclude(statu=4), many=True,
                               context={'request': self.context['request']}).data,
            RotorSerializer(obj.rotors.exclude(statu=4), many=True, context={'request': self.context['request']}).data,
            StatorSerializer(obj.stators.exclude(statu=4), many=True,
                             context={'request': self.context['request']}).data]
        return list(itertools.chain(*children))

    def get_tags(self, obj):
        return [item.name for item in obj.tags.all()]

    def get_detail(self, obj):
        return {
            'Phase Number': obj.phase_number,
            'Pole Pairs Number': obj.pole_pairs_number,
            'Turn Number': obj.turn_number,
            'Rated Voltage': obj.rated_voltage,
            'Rated Speed': obj.rated_speed,
        }

    class Meta:
        model = Motor
        fields = (
        'id', "name", 'sn', 'statu', 'memo', 'admin', 'health_indicator', 'lr_time', 'children', 'tags', 'detail')


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
    class Meta:
        model = Uphase
        fields = ('frequency',)


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
        return {'urms': obj.packs.last().ufeature.rms,
                'vrms': obj.packs.last().vfeature.rms,
                'wrms': obj.packs.last().wfeature.rms}

    def get_symfeatures(self, obj):
        return {
            'ns': obj.packs.last().symcomponent.n_sequence_rms,
            'ps': obj.packs.last().symcomponent.p_sequence_rms,
        }

    def get_psf(self, obj):
        phase_object = obj.packs.last().uphase
        trend_serializer = PSFserializer(phase_object, context={'request': self.context['request']})
        return trend_serializer.data

    class Meta:
        model = Motor
        fields = ('name', 'rmsfeatures', 'symfeatures', 'psf')


class IndexMotorCountSerializer(serializers.ModelSerializer):
    stator = serializers.SerializerMethodField()
    rotor = serializers.SerializerMethodField()
    bearing = serializers.SerializerMethodField()

    def get_stator(self, obj):
        return obj.stators.count()

    def get_bearing(self, obj):
        return obj.bearings.count()

    def get_rotor(self, obj):
        return obj.rotors.count()

    class Meta:
        model = Motor
        fields = ('name', 'stator', 'rotor', 'bearing')
