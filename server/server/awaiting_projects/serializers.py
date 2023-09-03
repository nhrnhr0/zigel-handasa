


from .models import AwaitingProject
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from client.models import Client

from client.serializers import ClientSelectSerializer

class AwaitingProjectSerializer(ModelSerializer):
    client__name = serializers.CharField(source='root_price_proposal.client.name', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='root_price_proposal.total')
    class Meta:
        model = AwaitingProject
        fields = ('id', 'name','client__name','last_comment','alert_date','created_at','updated_at','total',)

class AwaitingProjectDetailSerializer(ModelSerializer):
    client = ClientSelectSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    client_options = serializers.SerializerMethodField()
    def get_client_options(self, obj):
        return [{'value':client.id,'label':client.name} for client in Client.objects.all()]
    def get_comments(self, obj):
        return [comment.comment for comment in obj.comments.all()]
    class Meta:
        model = AwaitingProject
        fields = ('id', 'name','client','last_comment','alert_date','created_at','updated_at','total','comments','client_options',)