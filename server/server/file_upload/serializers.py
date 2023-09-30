from .models import FileUpload
from rest_framework import serializers


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'