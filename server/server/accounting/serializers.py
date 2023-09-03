
from .models import AccountingDoc
from rest_framework import serializers
class AccountingDocSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)
    client__name = serializers.CharField(source='client.name', read_only=True)
    type__name = serializers.SerializerMethodField()
    
    def get_type__name(self, obj):
        return obj.get_type_display()
    class Meta:
        model = AccountingDoc
        fields = ('id','client__name','doc_number','type','total','morning_id','created_at','type__name',)


