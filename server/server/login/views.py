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
from rest_framework.authtoken.models import Token
# Create your views here.
@api_view(["POST"])
def login(request):
    username=request.POST["userName"]
    password=request.POST["password"]
    user= authenticate(username=username,password=password)
    if user is not None:
        token,created= Token.objects.get_or_create(user=user)
        if not created:
            response_data={'token':token.key}
            return JsonResponse(response_data)
        else:
            return JsonResponse("somthing went wrong",safe=False)
    else:
        return JsonResponse("user does not exists",safe=False)

    