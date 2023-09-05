


from .models import AwaitingProject
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from client.models import Client
from client.serializers import ClientSelectSerializer

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
    client = ClientSelectSerializer(read_only=True)
    client_options = serializers.SerializerMethodField()
    api_data = serializers.SerializerMethodField()
    alert_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, allow_null=True)
    # if comments is None: we need to return an empty list
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        if obj.comments is None:
            return []
        return obj.comments
    
    def get_client_options(self, obj):
        return [{'value':client.id,'label':client.name} for client in Client.objects.all()]
    
    
    def get_api_data(self, obj):
        return obj.root_price_proposal.api_data
    class Meta:
        model = AwaitingProject
        fields = ('id', 'name','client','alert_date','created_at','updated_at','total','comments','client_options','api_data',)