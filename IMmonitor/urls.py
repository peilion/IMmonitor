"""IMmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls import url
import xadmin
from rest_framework.routers import DefaultRouter
from dashboard.views import *
from real_time.views import *
from rest_framework.documentation import include_docs_urls
from auth.views import LoginView, getUserInfo
from motors.views import DiagnosisPackRetrieveViewSet
from symmetry.views import PackListViewSet, DQPackListViewSet, FeatureThrendListViewSet, HarmonicsPackListViewSet, \
    EnvelopePackListViewSet

router = DefaultRouter()
router.register(r'motors', MotorsListViewSet, base_name='motors')
router.register(r'bearings', BearingListViewSet, base_name='bearings')
router.register(r'rotors', RotorListViewSet, base_name='rotors')
router.register(r'stators', StatorListViewSet, base_name='stators')
router.register(r'warningLog', WarningLogListViewSet, base_name='warning log')
router.register(r'weeklyrecord', WeeklyRecordListViewSet, base_name='Weekly record')
router.register(r'index-trend', MotorTrendRetriveViewset, base_name='Motor THD trend ')
router.register(r'index-radar', DashBoardMotorFeatureViewset, base_name='dash board radar')
router.register(r'index-bar', IndexMotorCountViewset, base_name='Motor component count')
router.register(r'motors/realtime', RealTimeMotorRetrieveViewset, base_name='Real Time Motor Condition')
router.register(r'packs', PackListViewSet, base_name='Motor Current Signal Packs')
router.register(r'dqpacks', DQPackListViewSet, base_name='DQ transformation')
router.register(r'feature-trend', FeatureThrendListViewSet, base_name='Feature Trend')
router.register(r'harmonics', HarmonicsPackListViewSet, base_name='Harmonics')
router.register(r'envelope', EnvelopePackListViewSet, base_name='Envelope')
router.register(r'diagnosis', DiagnosisPackRetrieveViewSet, base_name='Diagnosis')


urlpatterns = [
    path('ueditor/', include('DjangoUeditor.urls')),
    path('xadmin/', xadmin.site.urls),
    re_path('^', include(router.urls)),
    path('docs', include_docs_urls(title='Induction Motor Monitoring API')),
    path('index-treemap/', TreemMapView.as_view(), name='Tree map API'),
    path('imstatus/', MotorStatusView.as_view(), name='Motor statu overview API'),
    path('login', LoginView.as_view(), name='Login'),
    path('user/info', getUserInfo.as_view(), name='User info'),
    path('index-calendar/', IndexWarningCalendarView.as_view(), name='Calendar'),
    path('index-serverstatu/', IndexProgressBarView.as_view(), name='Table Statu'),
    path('silk/', include('silk.urls', namespace='silk')),

]
