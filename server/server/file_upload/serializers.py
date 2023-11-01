from .models import FileUpload
from rest_framework import serializers


class ProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'