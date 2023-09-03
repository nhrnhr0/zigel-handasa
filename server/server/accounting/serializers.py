
from .models import AccountingDoc
from rest_framework import serializers
class AccountingDocSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)
    client__name = serializers.CharField(source='client.name', read_only=True)
    type__name = serializers.SerializerMethodField()
    project__names = serializers.SerializerMethodField()
    def get_type__name(self, obj):
        return obj.get_type_display()
    
    def get_project__names(self, obj):
        ret = obj.root_price_proposals.all().values_list('root_project__name', flat=True).distinct()
        if len(ret) == 1:
            return ret[0]
        return ', '.join(ret)
    class Meta:
        model = AccountingDoc
        fields = ('id','client__name', 'project__names', 'doc_number','type','total','morning_id','created_at','type__name',)


