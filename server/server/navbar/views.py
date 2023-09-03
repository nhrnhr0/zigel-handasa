from django.shortcuts import render
from .models import Navbar
from .serializers import NavbarSerializer
from rest_framework import generics, permissions
from rest_framework import generics as geneeric
# Create your views here.
# class UserListView(generics.ListAPIView):


class NavbarListView(geneeric.ListAPIView):
    queryset = Navbar.objects.all()
    serializer_class = NavbarSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    