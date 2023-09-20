from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters
import django_filters.rest_framework
from project.models import Project
from project.serializers import ProjectSerializer
from core.filters import multiSelectFilterFactory,CreatedAtBetweenDateFilterBackend,UpdatedAtBetweenDateFilterBackend
from core.pagination import StandardResultsSetPagination
from rest_framework.decorators import api_view
from client.models import Client
from client.serializers import ClientSelectSerializer
from project.models import ProjectStatus
from project.views import ProjectStatusSelectSerializer

# Create your views here.
class DoneProjectListView(generics.ListAPIView):
    """
    View to list all projects in the system.

    * Requires token authentication.
    """
    queryset = Project.objects.select_related('root_price_proposal','root_price_proposal__client','status',).filter(closed=True)
    serializer_class = ProjectSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,
                       multiSelectFilterFactory('root_price_proposal__client__in'),multiSelectFilterFactory('status__in'),
                       CreatedAtBetweenDateFilterBackend,UpdatedAtBetweenDateFilterBackend]
    # filterset_fields = ['name','root_price_proposal__client']
    filterset_fields = {
        'name': ['icontains'],
        'created_at': ['lte','gte'],
        'updated_at': ['lte','gte'],
        'closed': ['exact'],
    }
    search_fields = ['name','root_price_proposal__client__name','root_price_proposal__total',]
    pagination_class = StandardResultsSetPagination
    
@api_view(['GET'])
def doneProjectsAPIDescription(request):
    clients_select = ClientSelectSerializer(Client.objects.all(),many=True).data
    status_select = ProjectStatusSelectSerializer(ProjectStatus.objects.all(),many=True).data
    # clients_select = ClientSelectSerializer(Client.objects.all(),many=True).data
    ret = {
        'extra':{
            'client_options':clients_select,
            'status_options':status_select,
        },
        'filters':{
            'name':{
                'type':'text',
                'name': 'שם',
                'slug': 'name',
            },
            'client':{
                'type':'multi-select',
                'options':'client_options',
                'name': 'לקוח',
                'slug': 'root_price_proposal__client',
            },
            'status':{ 
                'type':'multi-select',
                'options':'status_options',
                'name': 'סטטוס',
                'slug': 'status',
            },
            'created_at':{
                'type':'date',
                'name': 'נוצר בתאריך',
                'slug': 'created_at',
            },
            # 'updated_at':{
            #     'type':'date',
            #     'name': 'עודכן בתאריך',
            #     'slug': 'updated_at',
            # },
        },
        'fields': {
            'doc_number':{
                'lable': 'מספר מסמך',
                'sortable': True,
                'type': 'text',
            },
            'name':{
                'lable': 'תיאור',
                'sortable': True,
                'type': 'text',
            },
            'client__name': {
                'lable': 'לקוח',
                'sortable': True,
                'type': 'text',
            },
            'total_before_tax': {
                'lable': 'סה"כ (לפני מע"מ)',
                'sortable': True,
                'type': 'currency',
            },
            'last_comment': {
                'lable': 'הערה אחרונה',
                'sortable': True,
                'type': 'text',
            },
            'status__name': {
                'lable': 'סטטוס',
                'sortable': True,
                'type': 'text',
            },
            # 'order_number': {
            #     'lable': 'מספר הזמנה',
            #     'sortable': True,
            #     'type': 'text',
            # },
            'done-projects-action-cell': {
                'lable': 'פעולות',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'done-projects-action-cell',
            },
            'projects-progress-cell': {
                'lable': 'התקדמות',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'projects-progress-cell',
            },
            
            'created_at': {
                'lable': 'נוצר בתאריך',
                'sortable': True,
                'type': 'date',
            },
            # 'updated_at': {
            #     'lable': 'עודכן בתאריך',
            #     'sortable': True,
            #     'type': 'date',
            # },
            # 'test': {
            #     'lable': 'test',
            #     'sortable': False,
            #     'type': 'custom',
            #     'custom_component': 'test-component',
            # },
            # 'project-action-cell': {
            #     'lable': 'פעולות',
            #     'sortable': False,
            #     'type': 'custom',
            #     'custom_component': 'project-action-cell',
            # },
        },
        'actions':{
            'type':'None',
        },
    }
    from django.http import JsonResponse
    return JsonResponse({'api-description': ret})
