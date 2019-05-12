from django_filters.rest_framework import DjangoFilterBackend

from symmetry.filters import PackFilter
from motors.models import Motor, CurrentSignalPack
from symmetry.serializers import PackSerializer, PackListSerializer, DQPackSerializer, TrendSerializer, \
    HamonicsSerializer, EnvelopeSerializer
from rest_framework import mixins, viewsets
from rest_framework.response import Response
import collections
from collections import OrderedDict


# Create your views here.

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


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
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = TrendSerializer

    def get_queryset(self):
        queryset = CurrentSignalPack.objects.all().order_by('id')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        dic = {}
        for _ in serializer.data:
            for key, value in flatten(_).items():
                dic.setdefault(key, []).append(value)
        return Response(dic)


class HarmonicsPackListViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = HamonicsSerializer


class EnvelopePackListViewSet(HarmonicsPackListViewSet):
    serializer_class = EnvelopeSerializer
