
from .models import AccountingDoc, AccountingDocPriceProposal,AccountingDocRelation
from rest_framework import serializers
from project.models import Project




class AccountingDocRelationSerializerFlatParents(serializers.ModelSerializer):
    type = serializers.CharField(source='parent.get_type_display', read_only=True)
    doc_number = serializers.CharField(source='parent.doc_number', read_only=True)
    doc_date = serializers.CharField(source='parent.created_at', read_only=True)
    rel_total = serializers.DecimalField(source='total', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = AccountingDocRelation
        fields = ('id','rel_total','doc_number','type','total','doc_date',)

class AccountingDocRelationSerializerFlatChilds(serializers.ModelSerializer):
    type = serializers.CharField(source='child.get_type_display', read_only=True)
    doc_number = serializers.CharField(source='child.doc_number', read_only=True)
    doc_date = serializers.CharField(source='child.created_at', read_only=True)
    rel_total = serializers.DecimalField(source='total', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = AccountingDocRelation
        fields = ('id','rel_total','doc_number','type','total','doc_date',)


        
class ChildsAccountingDocRelationSerializer(serializers.ModelSerializer):
    doc_number = serializers.CharField(source='child.doc_number', read_only=True)
    doc_date = serializers.CharField(source='child.created_at', read_only=True)
    type = serializers.CharField(source='child.get_type_display', read_only=True)
    child_total = serializers.DecimalField(source='child.total_before_tax', read_only=True, max_digits=10, decimal_places=2)
    related_docs = serializers.SerializerMethodField()
    morning_id = serializers.CharField(source='child.morning_id', read_only=True)
    
    def get_related_docs(self, obj):
        # AccountingDocRelationSerializer for parents and childs
        parents = obj.child.parents.all()
        childs = obj.child.childs.all()
        parents_data = AccountingDocRelationSerializerFlatParents(parents, many=True).data
        childs_data = AccountingDocRelationSerializerFlatChilds(childs, many=True).data
        return {
            'parents': parents_data,
            'childs': childs_data,
        }
    class Meta:
        model = AccountingDocRelation
        fields = ('id','child','doc_number','type','total','doc_date','child_total','related_docs','morning_id',)

class RootPricePropProjectNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='root_project.name', read_only=True)
    class Meta:
        model = AccountingDocPriceProposal
        fields = ('name',)
        

class AccountingDocSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display', read_only=True)
    client__name = serializers.CharField(source='client.name', read_only=True)
    type__name = serializers.SerializerMethodField()
    project__names = serializers.SerializerMethodField()
    related_docs = serializers.SerializerMethodField()
    # childs = AccountingDocRelationSerializerFlatChilds(many=True, read_only=True)
    # parents = AccountingDocRelationSerializerFlatParents(many=True, read_only=True)
    
    def get_related_docs(self, obj):
        # AccountingDocRelationSerializer for parents and childs
        parents = obj.parents.all()
        childs = obj.childs.all()
        parents_data = AccountingDocRelationSerializerFlatParents(parents, many=True).data
        childs_data = AccountingDocRelationSerializerFlatChilds(childs, many=True).data
        return {
            'parents': parents_data,
            'childs': childs_data,
        }
    
    def get_project__names(self, obj):
        # ser = RootPricePropProjectNameSerializer(many=True, read_only=True, source='root_price_proposals', instance=obj)
        ser = RootPricePropProjectNameSerializer(many=True, read_only=True, instance=obj.root_price_proposals)
        data = ser.data
        for i in range(len(data)):
            data[i] = data[i]['name']
        return ', '.join(data)
    
    def get_type__name(self, obj):
        return obj.get_type_display()
    
    # def get_project__names(self, obj):
    #     ret = obj.root_price_proposals.all().values_list('root_project__name', flat=True).distinct()
    #     if len(ret) == 1:
    #         return ret[0]
    #     return ', '.join(ret)
    
    class Meta:
        model = AccountingDoc

        fields = ('id','client__name', 'project__names', 'doc_number','type','total','total_before_tax','morning_id','created_at','type__name','related_docs')



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


class ChildAccountingDocSerializer(serializers.ModelSerializer):
    doc_number = serializers.CharField(read_only=True)
    doc_date = serializers.CharField(source='created_at',read_only=True)
    type = serializers.CharField(source='get_type_display', read_only=True)
    total = serializers.DecimalField(source='total_before_tax', read_only=True, max_digits=10, decimal_places=2)
    class Meta:
        model = AccountingDoc
        fields = ('id','doc_number','type','total','doc_date',)

class ParentAccountingDocSerializer(serializers.ModelSerializer):
    doc_number = serializers.CharField(read_only=True)
    doc_date = serializers.CharField(source='created_at', read_only=True)
    type = serializers.CharField(source='get_type_display', read_only=True)
    total = serializers.DecimalField(source='total_before_tax', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = AccountingDoc
        fields = ('id','doc_number','type','total','doc_date',)

