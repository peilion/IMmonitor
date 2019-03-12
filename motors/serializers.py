from rest_framework import serializers
from motors.models import Motor, Bearing, Rotor, Stator, WarningLog, WeeklyRecord
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


class MotorTrendSerializer(serializers.ModelSerializer):
    trend = serializers.SerializerMethodField()

    def get_trend(self, obj):
        trend_json = {}
        motor = Motor.objects.filter(id=obj.id, )
        if motor:
            # 取到这个商品Queryset[0]
            signalpacks = motor[0].packs.all()
            u_thd_trend = []
            for pack in signalpacks:
                u_thd_trend.append(pack.ufeature.thd)
        return JSONRenderer(u_thd_trend)

    # 自定义获取方法
    def get_goods(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = Motor
        fields = ('name', 'statu')
