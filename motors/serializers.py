from rest_framework import serializers
from motors.models import Motor, Bearing, Rotor, Stator, WarningLog, WeeklyRecord, Ufeature, CurrentSignalPack, \
    Vfeature, Wfeature, SymComponent, Uphase, equip_types
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
import itertools
import numpy as np

ComponentSerializerFields = (
    'id', "name", 'equip_type', 'health_indicator', "statu", 'lr_time', 'tags', 'memo', 'admin')


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ComponentSerializer(serializers.ModelSerializer):
    # This class is built for inherit only!!

    admin = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        pass

    def get_admin(self, obj):
        return UserSeralizer(obj.motor.admin).data

    def update(self, instance, validated_data):
        # Patch Last repair time
        instance.lr_time = validated_data['lr_time']
        instance.save()
        return instance

    class Meta:
        fields = (
            'id', "name", 'equip_type', 'health_indicator', "statu", 'lr_time', 'tags', 'memo', 'admin', 'detail')


class BearingsSerializer(ComponentSerializer):
    def get_detail(self, obj):
        return {
            'Inner Race Diameter': obj.inner_race_diameter,
            'Inner Race Width': obj.inner_race_width,
            'Outter Race Diameter': obj.outter_race_diameter,
            'Outter Race Width': obj.outter_race_width,
            'Roller Diameter': obj.roller_diameter,
            'Roller Number': obj.roller_number,
            'Contact angle': obj.contact_angle,

        }

    class Meta:
        model = Bearing
        fields = ComponentSerializer.Meta.fields


class RotorSerializer(ComponentSerializer):
    def get_detail(self, obj):
        return {
            'Rotor Length': obj.length,
            'Outer Diameter': obj.outer_diameter,
            'Inner Diameter': obj.inner_diameter,
            'Slot Number': obj.slot_number,
        }

    class Meta:
        model = Rotor
        fields = ComponentSerializer.Meta.fields


class StatorSerializer(ComponentSerializer):
    def get_detail(self, obj):
        return {
            'Stator Length': obj.length,
            'Stator Diameter': obj.outer_diameter,
            'Stator Inner Diameter': obj.inner_diameter,
            'Slot Number': obj.slot_number,
        }

    class Meta:
        model = Rotor
        fields = ComponentSerializer.Meta.fields


class MotorsSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    admin = UserSeralizer(read_only=True)
    detail = serializers.SerializerMethodField()
    lr_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

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

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.lr_time = validated_data['lr_time']
        instance.save()
        return instance

    class Meta:
        model = Motor
        fields = (
            'id', "name", 'sn', 'statu', 'memo', 'lr_time', 'health_indicator', 'admin', 'children', 'tags', 'detail',
            'equip_type')


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


