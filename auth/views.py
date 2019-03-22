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
                'avatar': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2720094078,3198972262&fm=26&gp=0.jpg',
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
                'avatar': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2720094078,3198972262&fm=26&gp=0.jpg',
                'name': 'Super admin'
            }
        }
        return Response(userMap['admin'])
