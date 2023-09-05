from django.shortcuts import render
from rest_framework import generics

from client.serializers import ClientSelectSerializer
from .models import Project
from .serializers import ProjectDetailSerializer, ProjectSerializer
import django_filters
from rest_framework import filters
from core.filters import ClientMultiSelectFilter,StatusMultiSelectFilter
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
    queryset = Project.objects.select_related('client').all()
    serializer_class = ProjectSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,ClientMultiSelectFilter, StatusMultiSelectFilter]
    filterset_fields = ['name','client','created_at','updated_at',]
    search_fields = ['name','client__name','total',]
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
                'slug': 'client',
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
            'updated_at':{
                'type':'date',
                'name': 'עודכן בתאריך',
                'slug': 'updated_at',
            },
        },
        'fields': {
            'name':{
                'lable': 'שם',
                'sortable': True,
                'type': 'text',
            },
            'client__name': {
                'lable': 'לקוח',
                'sortable': True,
                'type': 'text',
            },
            'total': {
                'lable': 'סה"כ',
                'sortable': True,
                'type': 'text',
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
            'order_number': {
                'lable': 'מספר הזמנה',
                'sortable': True,
                'type': 'text',
            },
            'projects-action-cell': {
                'lable': 'פעולות',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'projects-action-cell',
            },
            'created_at': {
                'lable': 'נוצר בתאריך',
                'sortable': True,
                'type': 'date',
            },
            'updated_at': {
                'lable': 'עודכן בתאריך',
                'sortable': True,
                'type': 'date',
            },
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
class ProjectRetriveUpdateView(APIView):
    """
    View to list all projects in the system.

    * Requires token authentication.
    """
    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project,data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.data.get('client'):
                client = request.data.get('client')
                project.client_id = client
                
                status_data = request.data.get('status')
                if len(status_data) > 0:
                    status_data = status_data[0]
                    if status_data.get('value'):
                        project.status_id = status_data.get('value')
                    elif status_data.get('label'):
                        from project.models import ProjectStatus
                        project.status = ProjectStatus.objects.get_or_create(name=status_data.get('label'))[0]
                project.root_price_proposal.client_id = client
                project.root_price_proposal.total = request.data.get('total')
                project.root_price_proposal.save()
                project.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)