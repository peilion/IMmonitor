from django_filters.rest_framework import DjangoFilterBackend

from symmetry.filters import PackFilter
from motors.models import Motor, CurrentSignalPack
from motors.serializers import PackDiagnosisSerializer
from rest_framework import mixins, viewsets


class DiagnosisPackRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CurrentSignalPack.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filter_class = PackFilter
    serializer_class = PackDiagnosisSerializer
