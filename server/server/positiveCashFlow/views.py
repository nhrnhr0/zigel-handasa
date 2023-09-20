from django.shortcuts import render
from rest_framework import generics,permissions
from core.pagination import StandardResultsSetPagination
import django_filters.rest_framework
from rest_framework import filters
from accounting.models import AccountingDocInvoice
from positiveCashFlow.serializers import PositiveCashFlowInvoiceSerializer,PositiveCashFlowProjectSerializer
from rest_framework.response import Response
from client.models import Client
from rest_framework.decorators import api_view
from django.db.models import Count,Max
from django.db.models import F,FloatField, Sum, Subquery
from project.models import Project
from accounting.models import AccountingDocRelation
class PositiveCashFlowProjectView(generics.ListAPIView):
    # anotate my_childs=AccountingDocRelation.objects.filter(parent=obj.root_price_proposal).all()
    queryset = Project.objects.select_related('root_price_proposal','root_price_proposal__client','status',).prefetch_related('root_price_proposal','root_price_proposal__client','status',).all()
    serializer_class = PositiveCashFlowProjectSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [django_filters.rest_framework.
                          DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,]
    filterset_fields = {
        'name': ['icontains'],
        'created_at': ['lte','gte'],
        'updated_at': ['lte','gte'],
    }
    search_fields = ['name','root_price_proposal__client__name','root_price_proposal__total',]
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        queryset = self.paginate_queryset(queryset)
        ret = self.get_paginated_response(serializer.data)
        clients = Client.objects.all()
        client_options = []
        for client in clients:
            client_options.append({
                'label':client.name,
                'value':client.id,
            })
        
        max_childs_count = 0
        for project in ret.data['results']:
            if(len(project['recipts']) > max_childs_count):
                max_childs_count = len(project['recipts'])
        
        custom_data = {
            'max_childs_count':max_childs_count,
            'fields': {
                'client_name': {
                    'lable': 'לקוח',
                    'sortable': True,
                    'type': 'text',
                },
                'project_name': {
                    'lable': 'פרויקט',
                    'sortable': True,
                    'type': 'text',
                },
                'doc_numbers': {
                    'lable': 'מספר חשבוניות',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-project-doc-numbers',
                },
                'root_price_proposal__total_before_tax': {
                    'lable': 'סכום הפרויקט',
                    'sortable': False,
                    'type': 'currency',
                },
                'total_invoices_before_tax': {
                    'lable': 'סך חשבוניות לפני מע"מ',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-project-total-invoices-before-tax',
                },
                'total_receipts': {
                    'lable': 'סך קבלות לפני מע"מ',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-project-total-receipts',
                },
                'childs': {
                    'lable': 'קבלות',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-project-childs',
                    'colspan': max_childs_count,
                },
            },
            'filters': {
            'client': {
                'type':'multi-select',
                'options': 'client_options',
                'name': 'לקוח',
                'slug': 'client',
            },
            'created_at':{
                'type':'date',
                'name': 'נוצר בתאריך',
                'slug': 'created_at',
            },
        },
        'extra': {
            'client_options':client_options,
        },
    }
        ret.data['description'] = {'api-description': custom_data}
        return ret
    
    pass

class PositiveCashFlowInvoiceView(generics.ListAPIView):
    queryset = AccountingDocInvoice.objects.filter(active=True).annotate(project__name=F('root_price_proposals__root_project__name',)).select_related('client',).prefetch_related('childs','childs__child','root_price_proposals','root_price_proposals__root_project').all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [django_filters.rest_framework.
                       DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,]
    serializer_class = PositiveCashFlowInvoiceSerializer
    filterset_fields = {
        'doc_number': ['icontains'],
        'client': ['in'],
        'created_at': ['lte','gte'],
    }
    ordering_fields = {'doc_number':'doc_number','client__name':'client__name','created_at':'created_at','total_before_tax':'total_before_tax','project__name':'project__name',}
    
    search_fields = ['doc_number','client__name']
    # ordering_fields = {'doc_number':'doc_number','client__name':'client__name','created_at':'created_at','total_before_tax':'total_before_tax',}
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        max_childs_count = queryset.annotate(childs_count=Count('childs')).aggregate(Max('childs_count'))['childs_count__max']
        if(max_childs_count is None):
            max_childs_count = 0
        if (max_childs_count == 0):
            max_childs_count = 1

        queryset = self.paginate_queryset(queryset)
        ret = self.get_paginated_response(serializer.data)
        # Create the custom dictionary
        clients = Client.objects.all()
        client_options = []
        for client in clients:
            client_options.append({
                'label':client.name,
                'value':client.id,
            })
        custom_data = {
            'max_childs_count':max_childs_count,
            'fields': {
                'client__name': {
                    'lable': 'לקוח',
                    'sortable': True,
                    'type': 'text',
                },
                'project__name': {
                    'lable': 'פרויקט',
                    'sortable': True,
                    'type': 'text',
                },
                'doc_number': {
                    'lable': 'מספר חשבונית',
                    'sortable': True,
                    'type': 'text',
                },
                'total_before_tax': {
                    'lable': 'סכום חשבוניות לפני מע"מ',
                    'sortable': False,
                    'type': 'number',
                },
                'total_receipts': {
                    'lable': 'סך קבלות לפני מע"מ',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-invoice-total-receipts',
                },
                'childs': {
                    'lable': 'קבלות',
                    'sortable': False,
                    'type': 'custom',
                    'custom_component': 'positive-cash-flow-invoice-childs',
                    'colspan': max_childs_count,
                },
                
                'created_at': {
                    'lable': 'נוצר בתאריך',
                    'sortable': True,
                    'type': 'date',
                },
            },
            'filters': {
            'client': {
                'type':'multi-select',
                'options': 'client_options',
                'name': 'לקוח',
                'slug': 'client',
            },
            'created_at':{
                'type':'date',
                'name': 'נוצר בתאריך',
                'slug': 'created_at',
            },
        },
        'extra': {
            'client_options':client_options,
        },
        }
        ret.data['description'] = {'api-description': custom_data}

        # # Create the response dictionary
        # response_data = {
        #     **custom_data,
        #     'count': queryset.count(),
        #     'results': serializer.data,
        # }

        return ret
        
    pass