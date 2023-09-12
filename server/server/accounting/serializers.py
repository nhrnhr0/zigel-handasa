
from .models import AccountingDoc,AccountingDocRelation
from rest_framework import serializers
from project.models import Project

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

        fields = ('id','client__name', 'project__names', 'doc_number','type','total','total_before_tax','morning_id','created_at','type__name',)



class AccountingDocDetailSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)
    #client__name = serializers.CharField(source='client.name', read_only=True)
    # client_morning_id = serializers.CharField(source='client.morning_id', read_only=True)
    # client_emails = serializers.JSONField(source='client.emails', read_only=True)
    project__names = serializers.SerializerMethodField()
    # based_on = AccountingDocThroughDetailSerializer(many=True)
    # based_on = AccountingDocThroughDetailSerializer(source='based_on_set', many=True)
    linked_docs = serializers.SerializerMethodField()
    open_amount = serializers.SerializerMethodField()
    price_prop_order_numbers = serializers.SerializerMethodField()
    client_data = serializers.SerializerMethodField()
    
    def get_linked_docs(self, obj):
        ret = []
        for child_rel in obj.childs.all():
            ret.append({
                'id': child_rel.child.id,
                'doc_number': child_rel.child.doc_number,
                'total': child_rel.total,
            })
        return ret
        pass
    def get_open_amount(self, obj):
        return obj.get_open_amount()
    def get_price_prop_order_numbers(self, obj):
        # ret = obj.root_price_proposals.all().values_list('root_project__order_number', flat=True).distinct()
        projects = obj.root_price_proposals.all().values('root_project').distinct()
        ret = []
        for project_id in projects:
            
            project = Project.objects.get(id=project_id['root_project'])
            ret.append(project.order_number)

        return ret
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
        fields = ('id','linked_docs','price_prop_order_numbers','client_data', 'project__names', 'doc_number','type','total','total_before_tax','open_amount','morning_id','created_at','api_data',)
