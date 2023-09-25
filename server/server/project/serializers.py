
from rest_framework.serializers import ModelSerializer
from .models import Project
from rest_framework import serializers
from client.serializers import ClientSelectSerializer,get_all_clients_select

class ProjectSerializer(ModelSerializer):
    client__name = serializers.CharField(source='root_price_proposal.client.name', read_only=True)
    status__name = serializers.CharField(source='status.name', read_only=True)
    last_comment = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='root_price_proposal.total')
    total_before_tax = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='root_price_proposal.total_before_tax')
    total_invoices_before_tax = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_total_invoices_before_tax')
    doc_number = serializers.CharField(source='root_price_proposal.doc_number', read_only=True)
    morning_id = serializers.CharField(source='root_price_proposal.morning_id', read_only=True)
    def get_last_comment(self, obj):
        return obj.get_last_comment_text()
    class Meta:
        model = Project
        fields = ('id', 'name','total_invoices_before_tax','client__name','last_comment','created_at','updated_at','total','total_before_tax','status__name','order_number','doc_number','morning_id')
        

from client.models import Client
from project.models import ProjectStatus
class ProjectDetailSerializer(ModelSerializer):
    client = serializers.SerializerMethodField()
    client_options = serializers.SerializerMethodField()
    
    api_data = serializers.SerializerMethodField()
    
    status = serializers.SerializerMethodField()
    status_options = serializers.SerializerMethodField()
    
    comments = serializers.SerializerMethodField()
    
    def get_client(self, obj):
        if obj.root_price_proposal.client is None:
            return []
        return [{'value':obj.root_price_proposal.client.id,'label':obj.root_price_proposal.client.name}]
    
    def get_status(self, obj):
        if obj.status is None:
            return []
        return [{'value':obj.status.id,'label':obj.status.name}]
    
    def get_comments(self, obj):
        if obj.comments is None:
            return []
        return obj.comments
    def get_api_data(self, obj):
        return obj.root_price_proposal.api_data
    
    def get_client_options(self, obj):
        return get_all_clients_select()
    def get_status_options(self, obj):
        return [{'value':status.id,'label':status.name} for status in ProjectStatus.objects.all()]
    class Meta:
        model = Project
        fields = ('id', 'name','client','closed','created_at','updated_at','status','order_number','client_options','status_options','api_data','comments',)