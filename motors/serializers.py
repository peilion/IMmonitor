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

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('motor')
        return queryset

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


class URMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ufeature
        fields = ('rms',)


class VRMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vfeature
        fields = ('rms',)


class WRMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wfeature
        fields = ('rms',)


class SymFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymComponent
        fields = ('n_sequence_rms', 'p_sequence_rms')


class DashBoardRadarFeatureSerializer(serializers.ModelSerializer):
    ufeature = URMSSerializer(many=False)
    vfeature = VRMSSerializer(many=False)
    wfeature = WRMSSerializer(many=False)
    symcomp = SymFeatureSerializer(many=False)
    uphase = PSFserializer(many=False)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('ufeature')
        queryset = queryset.select_related('vfeature')
        queryset = queryset.select_related('wfeature')
        queryset = queryset.select_related('symcomp')
        queryset = queryset.select_related('uphase')
        return queryset

    class Meta:
        model = CurrentSignalPack
        fields = ('ufeature', 'vfeature', 'wfeature', 'symcomp', 'uphase')


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


class PackDiagnosisSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def get_result(self, obj):
        mean = [4.08730257e+01, 1.73987679e-01, 3.38665858e-02, 2.51566228e-02
            , 1.38076468e-02, 8.69973561e-03, 8.03956150e-03, 5.46600118e-03
            , 5.47209168e-03, 3.97664006e-03, 3.49551548e-03, 3.12332230e-03
            , 2.89882393e-03, 2.59235078e-03, 2.44827813e-03, 2.21258332e-03
            , 2.06736559e-03, 1.94553804e-03, 1.83568153e-03, 1.71402076e-03
            , 1.63825834e-03, 1.92515618e-13, 1.71528731e+00, 1.87438023e+00
            , 1.17415829e+00, 3.02615524e+00, 1.10859131e+00, 3.56888253e+00
            , 1.40528613e+00, 3.43715517e+00, 1.35946774e+00]
        var = [6.86443163e+01, 1.37727184e-04, 8.18211372e-05, 3.84386914e-05
            , 2.45116228e-05, 1.15764157e-05, 1.53705260e-05, 6.06259742e-06
            , 8.01371761e-06, 3.43112622e-06, 2.69436399e-06, 2.23925042e-06
            , 1.89684885e-06, 1.54081806e-06, 1.34945087e-06, 1.15557906e-06
            , 9.93618765e-07, 8.75660264e-07, 7.92424842e-07, 7.10468212e-07
            , 6.40105019e-07, 2.29148844e-26, 1.43297362e+00, 1.06251902e+00
            , 3.88808295e-01, 7.86609996e+00, 2.75726200e-01, 1.51483484e+01
            , 6.90431391e-01, 1.44584506e+01, 4.40973639e-01]
        data = np.concatenate(([obj.uphase.frequency, obj.ufeature.rms, obj.ufeature.thd],
                               np.fromstring(obj.ufeature.harmonics), np.fromstring(obj.ufeature.fbrb)))

        import pickle
        f2 = open('db_tools/MLmodel/svm-rbf.txt', 'rb')
        s2 = f2.read()
        clf2 = pickle.loads(s2)
        result = clf2.predict(np.reshape(((data - mean) / np.sqrt(var)), (1, -1)))
        return int(result)

    class Meta:
        model = CurrentSignalPack
        fields = "__all__"
