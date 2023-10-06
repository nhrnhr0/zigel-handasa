from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from base_project.models import BaseProject
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.
@api_view(["POST"])
def login(request):
    username=request.POST["userName"]
    password=request.POST["password"]
    user= authenticate(username=username,password=password)
    current_user=User.objects.get(username=username)
    if user is not None:
        return JsonResponse("user exists",safe=False)
    else:
        return JsonResponse("user does not exists",safe=False)

    