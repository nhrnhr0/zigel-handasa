from django.shortcuts import render

from rest_framework import generics, permissions
from .serializers import AccountingDocSerializer
from .models import AccountingDoc
import django_filters
from rest_framework import filters
from core.filters import CreatedAtBetweenDateFilterBackend, UpdatedAtBetweenDateFilterBackend
from client.models import Client
from core.pagination import StandardResultsSetPagination
from core.filters import ClientMultiSelectFilter, TypeMultiSlectFilter
from project.models import Project
class AccountingDocListView(generics.ListAPIView):
    queryset = AccountingDoc.objects.select_related('client').filter(active=True)
    serializer_class = AccountingDocSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,CreatedAtBetweenDateFilterBackend,UpdatedAtBetweenDateFilterBackend,CreatedAtBetweenDateFilterBackend,ClientMultiSelectFilter,TypeMultiSlectFilter]
    search_fields = ['client__name','total','type','doc_number',]
    pagination_class = StandardResultsSetPagination

    pass
from .models import FINANCIAL_DOC_TYPES
def accountingDocsAPIDescription(request):
    clients = Client.objects.all()
    client_options = [{'value':client.id,'label':client.name} for client in clients]
    for i in FINANCIAL_DOC_TYPES:
        print(i)
    type_options = [{'value':i[0],'label':i[1]} for i in FINANCIAL_DOC_TYPES]

    project_options = [{'value':i.id,'label':i.name} for i in Project.objects.all()]

    ret = {
        'extra':{
            'client_options':client_options,
            'type_options':type_options,
            'project_options':project_options,
        },
        'filters':{
            'client':{
                'type':'multi-select',
                'options':'client_options',
                'name': 'לקוח',
                'slug': 'client',
            },
            'type': {
                'type':'multi-select',
                'options': 'type_options',
                'name': 'סוג',
                'slug': 'type',
            },
            'project': {
                'type':'multi-select',
                'options': 'project_options',
                'name': 'פרויקט',
                'slug': 'project',
            },
            'created_at':{
                'type':'date',
                'name': 'נוצר בתאריך',
                'slug': 'created_at',
            },
        },
        'fields': {
            
            'doc_number': {
                'lable': 'מספר מסמך',
                'sortable': True,
                'type': 'text',
            },
            'type__name': {
                'lable': 'סוג',
                'sortable': True,
                'type': 'text',
            },
            'client__name': {
                'lable': 'לקוח',
                'sortable': True,
                'type': 'text',
            },
            'project__names': {
                'lable': 'פרויקט',
                'sortable': True,
                'type': 'text',
            },
            'total': {
                'lable': 'סה"כ',
                'sortable': True,
                'type': 'text',
            },
            'created_at': {
                'lable': 'נוצר בתאריך',
                'sortable': True,
                'type': 'date',
            },
            
        },
        'actions':{
        },
    }
    from django.http import JsonResponse
    return JsonResponse({'api-description': ret})

from .serializers import AccountingDocDetailSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(["GET"])
def get_accounting_docs_morning_info(request):
    morning_ids = request.GET.get('morning_ids[]')
    morning_ids = morning_ids.split(',')
    from accounting.models import AccountingDoc
    docs = AccountingDoc.objects.filter(morning_id__in=morning_ids)
    return JsonResponse({'docs':AccountingDocDetailSerializer(docs,many=True).data})