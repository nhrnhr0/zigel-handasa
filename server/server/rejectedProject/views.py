from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RejectedProjectDetailSerializer, RejectedReasonSelectSerializer
from .models import RejectedReason

from rest_framework import generics
from .models import RejectedReason, RejectedProject
from .serializers import RejectedProjectSerializer, RejectedReasonSelectSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters
from core.filters import ClientMultiSelectFilter,ReasonMultiSelectFilter
from core.pagination import StandardResultsSetPagination
# Create your views here.
from client.models import Client
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
class RejectedReasonSelectView(generics.ListAPIView):
    """
    View to list all rejected reasons in the system.

    * Requires token authentication.
    """
    queryset = RejectedReason.objects.all()
    serializer_class = RejectedReasonSelectSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    
    
class RejectedProjectListView(generics.ListAPIView):
    queryset = RejectedProject.objects.select_related('reason').all()
    serializer_class = RejectedProjectSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,ClientMultiSelectFilter,ReasonMultiSelectFilter]
    # filterset_fields = ['name','client','reason','created_at','updated_at',]
    # search_fields = ['name','client__name','last_comment','reason__name',]
    pagination_class = StandardResultsSetPagination
    pass

@api_view(['GET'])
def rejectedProjectsAPIDescription(request):
    clients = Client.objects.all()
    client_options = [{'value':client.id,'label':client.name} for client in clients]
    resasons = RejectedReason.objects.all()
    reason_options = [{'value':reason.id,'label':reason.name} for reason in resasons]
    
    ret = {
        'extra':{
            'client_options':client_options,
            'reason_options':reason_options,
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
            'reason':{
                'type':'multi-select',
                'options':'reason_options',
                'name': 'סיבה',
                'slug': 'reason',
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
            'doc_number': {
                'lable': 'מספר מסמך',
                'sortable': True,
                'type': 'text',
            },
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
            'reason': {
                'lable': 'סיבה',
                'sortable': True,
                'type': 'text',
            },
            'edit': {
                'lable': 'עריכה',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'rejected-project-edit-button',
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
        },
        'actions':{
        },
    }
    from django.http import JsonResponse
    return JsonResponse({'api-description': ret})

@api_view(['POST'])
def rejectedProjectApproveView(request, pk):
    from rejectedProject.models import RejectedProject
    from awaiting_projects.models import AwaitingProject
    from datetime import datetime, timedelta
    from django.utils.timezone import make_aware
    import pytz
    rejectedProject = get_object_or_404(RejectedProject, pk=pk)
    name = rejectedProject.name
    alert_date = datetime.now() + timedelta(days=7)
    alert_date = make_aware(alert_date, timezone=pytz.timezone("Asia/Jerusalem"))

    root_price_proposal = rejectedProject.root_price_proposal
    # project = Project.objects.create(
    #     name=obj.name,
    #     order_number=order_number,
    # )
    
    # project.copy_base_project_data(obj)
    awaiting_project = AwaitingProject.objects.create(
        name=name,
        alert_date=alert_date,
    )
    awaiting_project.copy_base_project_data(rejectedProject)
    
    rejectedProject.delete()
    awaiting_project.root_price_proposal = root_price_proposal
    root_price_proposal.save()
    awaiting_project.save()
    
    return Response(status=status.HTTP_200_OK)

class RejectedProjectRetriveUpdateView(APIView):
    class_serializer = RejectedProjectDetailSerializer
    def get(self, request: Request, pk: int):
        print('get')
        obj = get_object_or_404(RejectedProject, pk=pk)
        serializer = self.class_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, pk: int):
        print('put')
        obj = get_object_or_404(RejectedProject, pk=pk)
        serializer = self.class_serializer(obj, data=request.data)
        if serializer.is_valid():
            saved_obj = serializer.save()
            if len(request.data['client']) > 0:
                saved_obj.client_id = request.data['client'][0]['value']
                saved_obj.root_price_proposal.client_id = request.data['client'][0]['value']
            
            saved_obj.root_price_proposal.total = request.data['api_data']['total']
            saved_obj.root_price_proposal.api_data = request.data['api_data']
            saved_obj.root_price_proposal.api_data['description'] = request.data['name']
            saved_obj.root_price_proposal.save()
            saved_obj.comments = request.data['comments']
            
            saved_obj.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)