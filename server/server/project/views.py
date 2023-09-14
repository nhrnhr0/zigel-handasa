from django.shortcuts import render
from rest_framework import generics

from client.serializers import ClientSelectSerializer
from .models import Project
from .serializers import ProjectDetailSerializer, ProjectSerializer
import django_filters
from rest_framework import filters
from core.filters import ClientMultiSelectFilter,StatusMultiSelectFilter,multiSelectFilterFactory,CreatedAtBetweenDateFilterBackend,UpdatedAtBetweenDateFilterBackend
from core.pagination import StandardResultsSetPagination
# Create your views here.
from project.models import ProjectStatus
from rest_framework import serializers
class ProjectStatusSelectSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')
    class Meta:
        model = ProjectStatus
        fields = ('value','label',)

class ProjectListView(generics.ListAPIView):
    """
    View to list all projects in the system.

    * Requires token authentication.
    """
    queryset = Project.objects.select_related('root_price_proposal','root_price_proposal__client','status',).all()
    serializer_class = ProjectSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,
                       multiSelectFilterFactory('root_price_proposal__client__in'),multiSelectFilterFactory('status__in'),
                       CreatedAtBetweenDateFilterBackend,UpdatedAtBetweenDateFilterBackend]
    # filterset_fields = ['name','root_price_proposal__client']
    filterset_fields = {
        'name': ['icontains'],
        'created_at': ['lte','gte'],
        'updated_at': ['lte','gte'],
    }
    search_fields = ['name','root_price_proposal__client__name','root_price_proposal__total',]
    pagination_class = StandardResultsSetPagination
    # permission_classes = (permissions.IsAuthenticated,)
from rest_framework.decorators import api_view
from client.models import Client
@api_view(['GET'])
def projectsAPIDescription(request):
    pass
    list_view = ProjectListView
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
            'projects-action-cell': {
                'lable': 'פעולות',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'projects-action-cell',
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



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProjectRetriveUpdateView(APIView):
    class_serializer = ProjectDetailSerializer

    """
    View to list all projects in the system.

    * Requires token authentication.
    """
    def get(self, request, pk):
        obj = get_object_or_404(Project,pk=pk)
        serializer = self.class_serializer(obj)
        return Response(serializer.data)
    def put(self, request, pk):
        errors = []
        print('put')
        saved_obj = get_object_or_404(Project, pk=pk)
        # serializer = self.class_serializer(obj, data=request.data)
        saved_obj.name = request.data['name']
        saved_obj.order_number = request.data['order_number']
        if len(request.data['client']) > 0:
            saved_obj.client_id = request.data['client'][0]['value']
            saved_obj.root_price_proposal.client_id = request.data['client'][0]['value']
            
        if len(request.data['status']) > 0:
            status_data = request.data['status'][0]
            if status_data.get('value'):
                saved_obj.status_id = status_data.get('value')
            elif status_data.get('label'):
                from project.models import ProjectStatus
                saved_obj.status = ProjectStatus.objects.get_or_create(name=status_data.get('label'))[0]
        
        saved_obj.root_price_proposal.total = request.data['api_data']['total']
        saved_obj.root_price_proposal.api_data = request.data['api_data']
        saved_obj.root_price_proposal.save()
        saved_obj.comments = request.data['comments']
        saved_obj.save()
        serializer = self.class_serializer(saved_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET'])
def get_project_accounting_docs(request,pk):
    from accounting.models import AccountingDoc, AccountingDocRelation
    from accounting.serializers import ChildsAccountingDocRelationSerializer
    obj = get_object_or_404(Project,pk=pk)
    price_prop = obj.root_price_proposal
    docs = AccountingDocRelation.objects.filter(parent=price_prop)
    print(docs)
    serializer = ChildsAccountingDocRelationSerializer(docs,many=True)
    data = serializer.data
    return Response(data)

    
    pass