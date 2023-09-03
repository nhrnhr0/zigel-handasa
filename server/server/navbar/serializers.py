

from .models import Navbar
from rest_framework import serializers

class NavbarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar
        fields = ('id', 'name', 'url','order',)

        