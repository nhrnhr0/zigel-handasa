
from rest_framework.serializers import ModelSerializer
from .models import Project
from rest_framework import serializers
class ProjectSerializer(ModelSerializer):
    client__name = serializers.CharField(source='client.name', read_only=True)
    status__name = serializers.CharField(source='status.name', read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name','client__name','last_comment','created_at','updated_at','total','status__name','order_number')

from client.models import Client
from project.models import ProjectStatus
class ProjectDetailSerializer(ModelSerializer):
    client_options = serializers.SerializerMethodField()
    status_options = serializers.SerializerMethodField()
    
    def get_client_options(self, obj):
        return [{'value':client.id,'label':client.name} for client in Client.objects.all()]
    def get_status_options(self, obj):
        return [{'value':status.id,'label':status.name} for status in ProjectStatus.objects.all()]
    class Meta:
        model = Project
        fields = ('id', 'name','client','last_comment','created_at','updated_at','total','status','order_number','client_options','status_options',)