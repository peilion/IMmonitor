import django_filters
from motors.models import CurrentSignalPack

class PackFilter(django_filters.rest_framework.FilterSet):
    time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = CurrentSignalPack
        fields = ['time','motor', ]