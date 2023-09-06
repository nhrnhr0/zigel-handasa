


from .models import AwaitingProject
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from client.models import Client
from client.serializers import ClientSelectSerializer,get_all_clients_select

class AwaitingProjectSerializer(ModelSerializer):
    client__name = serializers.CharField(source='root_price_proposal.client.name', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='root_price_proposal.total')
    last_comment_text = serializers.SerializerMethodField()
    
    def get_last_comment_text(self, obj):
        return obj.get_last_comment_text()
    class Meta:
        model = AwaitingProject
        fields = ('id', 'name','client__name','last_comment_text','alert_date','created_at','updated_at','total',)

class AwaitingProjectDetailSerializer(ModelSerializer):
    client = serializers.SerializerMethodField()
    client_options = serializers.SerializerMethodField()
    api_data = serializers.SerializerMethodField()
    alert_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, allow_null=True)
    # if comments is None: we need to return an empty list
    comments = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='root_price_proposal.total')
    
    def get_client(self, obj):
        # to hanle multiselect we return [clientSerializer] and not clientSerializer
        return [ClientSelectSerializer(obj.root_price_proposal.client, read_only=True).data]
    def get_comments(self, obj):
        if obj.comments is None:
            return []
        return obj.comments
    
    def get_client_options(self, obj):
        return get_all_clients_select()
    
    
    def get_api_data(self, obj):
        return obj.root_price_proposal.api_data
    class Meta:
        model = AwaitingProject
        fields = ('id', 'name','client','alert_date','created_at','updated_at','total','comments','client_options','api_data',)