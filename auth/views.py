from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(APIView):

    def post(self, request, format=None):
        userMap = {
            'admin': {
                'roles': ['admin'],
                'token': 'admin',
                'introduction': 'This is superuser',
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'name': 'Super admin'
            }
        }
        return Response(userMap['admin'])


class getUserInfo(APIView):

    def get(self, request):
        userMap = {
            'admin': {
                'roles': ['admin'],
                'token': 'admin',
                'introduction': 'This is superuser',
                'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                'name': 'Super admin'
            }
        }
        return Response(userMap['admin'])
