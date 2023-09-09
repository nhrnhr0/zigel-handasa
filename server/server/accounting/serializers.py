
from .models import AccountingDoc,AccountingDocRelation
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


class AccountingDocThroughDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model: AccountingDocRelation
        fields = ('total',)

class AccountingDocDetailSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)
    #client__name = serializers.CharField(source='client.name', read_only=True)
    # client_morning_id = serializers.CharField(source='client.morning_id', read_only=True)
    # client_emails = serializers.JSONField(source='client.emails', read_only=True)
    type__name = serializers.SerializerMethodField()
    project__names = serializers.SerializerMethodField()
    based_on = AccountingDocThroughDetailSerializer
    related_to = AccountingDocThroughDetailSerializer
    
    client_data = serializers.SerializerMethodField()
    
    def get_client_data(self, obj):
        return obj.client.get_data()
    def get_type__name(self, obj):
        return obj.get_type_display()
    
    def get_project__names(self, obj):
        ret = obj.root_price_proposals.all().values_list('root_project__name', flat=True).distinct()
        if len(ret) == 1:
            return ret[0]
        return ', '.join(ret)
    class Meta:
        model = AccountingDoc
        fields = ('id','client_data', 'project__names', 'doc_number','type','total','morning_id','created_at','type__name','api_data','based_on','related_to',)
