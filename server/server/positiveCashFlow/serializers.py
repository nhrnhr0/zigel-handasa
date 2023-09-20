

from rest_framework.fields import empty
from accounting.models import AccountingDocInvoice, AccountingDocRelation,AccountingDocReceipt
from rest_framework import serializers
from project.models import Project
from decimal import Decimal
from django.db.models import Count,Max,Sum

class PositiveCashFlowProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='root_price_proposal.client.name', read_only=True)
    project_name = serializers.CharField(source='name', read_only=True)
    doc_numbers = serializers.SerializerMethodField()
    total_invoices_before_tax = serializers.SerializerMethodField()
    # childs = serializers.SerializerMethodField()
    # def get_childs(self, obj):
    #     all_reciepts = AccountingDocRelation.objects.filter(parent=obj.root_price_proposal).all()
    #     return PositiveCashFlowReciptSerializer(all_reciepts, many=True).data
    recipts = serializers.SerializerMethodField()
    root_price_proposal__total = serializers.DecimalField(source='root_price_proposal.total', read_only=True, max_digits=10, decimal_places=2)
    root_price_proposal__total_before_tax = serializers.DecimalField(source='root_price_proposal.total_before_tax', read_only=True, max_digits=10, decimal_places=2)
    all_invoices = {}
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        
    def get_recipts(self, obj):
        self.set_all_invoices_if_needed(obj)
        all_invoices = self.all_invoices[obj.id]
        all_reciepts = AccountingDocRelation.objects.filter(parent__in=all_invoices).all()
        return PositiveCashFlowReciptSerializer(all_reciepts, many=True).data
    def get_doc_numbers(self, obj):
        self.set_all_invoices_if_needed(obj)
        return [{'doc_number': invoice.doc_number, 'date': invoice.created_at, 'total_before_tax': invoice.total_before_tax} for invoice in self.all_invoices[obj.id]]
    def set_all_invoices_if_needed(self, obj):
        if self.all_invoices.get(obj.id, None) is None:
            t = AccountingDocInvoice.objects.filter(root_price_proposals__root_project=obj).all()
            self.all_invoices[obj.id] = t
    
    def get_total_invoices_before_tax(self, obj):
        ret = self.all_invoices[obj.id].aggregate(Sum('total'))['total__sum']
        if ret is None:
            return 0
        return ret / Decimal(1.17)
    
    class Meta:
        model = Project
        fields = ('id','client_name','project_name','doc_numbers','root_price_proposal__total','root_price_proposal__total_before_tax','total_invoices_before_tax','recipts',)

class PositiveCashFlowReciptSerializer(serializers.ModelSerializer):
    doc_number = serializers.CharField(source='child.doc_number', read_only=True)
    doc_date = serializers.CharField(source='child.created_at', read_only=True)
    type = serializers.CharField(source='child.get_type_display', read_only=True)
    rel_total = serializers.DecimalField(source='total', read_only=True, max_digits=10, decimal_places=2)
    total = serializers.DecimalField(source='child.total_before_tax', read_only=True, max_digits=10, decimal_places=2)
    class Meta:
        model = AccountingDocRelation
        fields = ('id','rel_total','doc_number','type','doc_date','total',)
    pass

class PositiveCashFlowInvoiceSerializer(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.name', read_only=True)
    project__name = serializers.SerializerMethodField()
    childs = serializers.SerializerMethodField()
    def get_project__name(self, obj):
        ret = obj.root_price_proposals.all().values_list('root_project__name', flat=True)
        return ', '.join(ret)
    class Meta:
        model = AccountingDocInvoice
        fields = ('id','client__name','project__name','doc_number','total','total_before_tax','created_at','childs',)
        
    def get_childs(self, obj):
        return PositiveCashFlowReciptSerializer(obj.childs.all(), many=True).data
    
        
