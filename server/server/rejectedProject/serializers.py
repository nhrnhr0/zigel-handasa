
from rest_framework import serializers
from .models import RejectedProject, RejectedReason
class RejectedReasonSelectSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name', read_only=True)
    value = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = RejectedReason
        fields = ('label', 'value',)
    
class RejectedProjectSerializer(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.name', read_only=True)
    reason__name = serializers.CharField(source='reason.name', read_only=True)
    class Meta:
        model = RejectedProject
        fields = ('id', 'name','client__name','last_comment','reason__name','created_at','updated_at',)