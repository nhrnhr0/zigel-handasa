from .models import Client
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name',)


class ClientSelectSerializer(ModelSerializer):
    label = serializers.CharField(source='name', read_only=True)
    value = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Client
        fields = ('value', 'label',)