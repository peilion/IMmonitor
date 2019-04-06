from django_filters.rest_framework import DjangoFilterBackend

from symmetry.filters import PackFilter
from motors.models import Motor, CurrentSignalPack
from symmetry.serializers import PackSerializer, PackListSerializer, DQPackSerializer, TrendSerializer, \
    HamonicsSerializer, EnvelopeSerializer
from rest_framework import mixins, viewsets


# Create your views here.
class PackListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PackSerializer
        return PackListSerializer


class DQPackListViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = DQPackSerializer


class FeatureThrendListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = TrendSerializer


class HarmonicsPackListViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = HamonicsSerializer


class EnvelopePackListViewSet(HarmonicsPackListViewSet):
    serializer_class = EnvelopeSerializer
