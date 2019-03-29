from motors.models import Motor
from real_time.serializers import RealTimeMotorSerializer
from rest_framework import mixins, viewsets


# Create your views here.
class RealTimeMotorRetrieveViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Motor.objects.all().order_by('id')
    serializer_class = RealTimeMotorSerializer
