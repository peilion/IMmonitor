import django_filters
from motors.models import Motor, WarningLog,WeeklyRecord


class MotorsFilter(django_filters.rest_framework.FilterSet):
    statu = django_filters.ChoiceFilter(choices=Motor.asset_status)

    class Meta:
        model = Motor
        fields = ['statu']


class WarninglogFilter(django_filters.rest_framework.FilterSet):
    # motor = django_filters.CharFilter(lookup_expr='icontains')
    severity = django_filters.ChoiceFilter(choices=WarningLog.severity_choice)

    class Meta:
        model = WarningLog
        fields = ['motor', ]


class WeeklyRecordFilter(django_filters.rest_framework.FilterSet):
    # motor = django_filters.CharFilter(lookup_expr='icontains')
    c_day = django_filters.DateFromToRangeFilter()

    class Meta:
        model = WeeklyRecord
        fields = ['c_day', ]
