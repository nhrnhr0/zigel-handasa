from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework import generics

from rejectedProject.models import RejectedReason
from .models import AwaitingProject
from .serializers import AwaitingProjectSerializer
import django_filters.rest_framework
from rest_framework import filters

from core.filters import BaseDateFilter

from django_filters import rest_framework
from rest_framework.decorators import api_view
from core.pagination import StandardResultsSetPagination
from core.filters import MultiSelectFilter, CreatedAtBetweenDateFilterBackend, UpdatedAtBetweenDateFilterBackend,multiSelectFilterFactory

class AwaitingProjectsListView(generics.ListAPIView):
    queryset = AwaitingProject.objects.select_related('root_price_proposal__client', 'root_price_proposal').all()
    serializer_class = AwaitingProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,]
    # filterset_fields = ['name','created_at','updated_at',{'alert_date':['lte','gte']},]
    filterset_fields = {
        'name': ['icontains'],
        'root_price_proposal__client': ['in'],
        'root_price_proposal__doc_number': ['icontains'],
        'created_at': ['lte','gte'],
        'updated_at': ['lte','gte'],
        'alert_date': ['lte','gte'],
    }
    search_fields = ['name','root_price_proposal__client__name','comments','root_price_proposal__doc_number', 'root_price_proposal__totoal_before_tax']
    pagination_class = StandardResultsSetPagination
    
    # if /awaiting-projects/?overdue=true we need to filter by alert_date__lte=now
    def get_queryset(self):
        from django.utils import timezone
        queryset = super().get_queryset()
        if self.request.query_params.get('overdue', None) == 'true':
            queryset = queryset.filter(alert_date__lte=timezone.now())
        return queryset

from client.models import Client

@api_view(['GET'])
def awaitingProjectsAPIDescription(request):
    clients = Client.objects.all()
    client_options = [{'value':client.id,'label':client.name} for client in clients]
    
    ret = {
        'extra':{
            'client_options':client_options,
        },
        'filters':{
            'doc_number':{
                'type':'text',
                'name': 'מספר מסמך',
                'slug': 'root_price_proposal__doc_number__icontains', # TODO
            },
            'name':{
                'type':'text',
                'name': 'תיאור',
                'slug': 'name__icontains',
            },
            'client':{
                'type':'multi-select',
                'options':'client_options',
                'name': 'לקוח',
                'slug': 'root_price_proposal__client',
            },
            'alrt_date':{
                'type':'date',
                'name': 'תאריך התראה',
                'slug': 'alert_date',
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
            'awaiting-projects-action-cell': {
                'lable': 'פעולות',
                'sortable': False,
                'type': 'custom',
                'custom_component': 'awaiting-projects-action-cell',
            },
            # 'created_at': {
            #     'lable': 'נוצר בתאריך',
            #     'sortable': True,
            #     'type': 'date',
            # },
            # 'updated_at': {
            #     'lable': 'עודכן בתאריך',
            #     'sortable': True,
            #     'type': 'date',
            # },
            'alert_date': {
                'lable': 'תאריך התראה',
                'sortable': True,
                'type': 'custom',
                'custom_component': 'awaiting-projects-alert-date-cell',
            },
            'last_comment_text': {
                'lable': 'הערה אחרונה',
                'sortable': True,
                'type': 'text',
            },
        },
        'actions':{
            'type':'None',
        },
    }
    from django.http import JsonResponse
    return JsonResponse({'api-description': ret})

from .serializers import AwaitingProjectDetailSerializer
from rest_framework.generics import RetrieveUpdateAPIView
# class AwaitingProjectsDetailView(RetrieveUpdateAPIView):
#     # mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
#     queryset = AwaitingProject.objects.all()
#     serializer_class = AwaitingProjectDetailSerializer
    
#     def get(self, request, *args, **kwargs):
#         print('get')
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         print('put')
#         return self.update(request, *args, **kwargs)
    
from rest_framework.views import APIView
from rest_framework.request import Request
from awaiting_projects.models import AwaitingProject
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from project.models import Project
from rest_framework.decorators import api_view

class AwaitingProjectRetriveUpdateView(APIView):
    class_serializer = AwaitingProjectDetailSerializer
    def get(self, request: Request, pk: int):
        print('get')
        obj = get_object_or_404(AwaitingProject, pk=pk)
        serializer = self.class_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, pk: int):
        print('put')
        obj = get_object_or_404(AwaitingProject, pk=pk)
        serializer = self.class_serializer(obj, data=request.data)
        if serializer.is_valid():
            saved_obj = serializer.save()
            if len(request.data['client']) > 0:
                saved_obj.client_id = request.data['client'][0]['value']
                saved_obj.root_price_proposal.client_id = request.data['client'][0]['value']
            
            saved_obj.root_price_proposal.total = request.data['api_data']['total']
            saved_obj.root_price_proposal.api_data = request.data['api_data']
            saved_obj.root_price_proposal.save()
            saved_obj.comments = request.data['comments']
            saved_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def awaitingProjectSnoozeView(request, pk):
    obj = get_object_or_404(AwaitingProject, pk=pk)
    print(request.data)
    number_of_days = request.data['number_of_days']
    # if str, convert to int
    if type(number_of_days) == str:
        number_of_days = int(number_of_days)

    from datetime import timedelta, datetime
    from django.utils import timezone
    obj.alert_date = timezone.now() + timedelta(days=number_of_days)
    obj.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def awaitingProjectApproveView(request, pk):
    obj = get_object_or_404(AwaitingProject, pk=pk)
    order_number = request.data['order_number']
    root_price_proposal = obj.root_price_proposal
    project = Project.objects.create(
        name=obj.name,
        order_number=order_number,
    )
    
    project.comments = obj.comments
    
    obj.delete()
    root_price_proposal.active = True
    
    
    project.root_price_proposal = root_price_proposal
    root_price_proposal.save()
    project.save()
    # root_price_proposal.project = project
    # root_price_proposal.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def awaitingProjectRejectView(request, pk):
    obj = get_object_or_404(AwaitingProject, pk=pk)
    if type(request.data) == dict:
        reason_text = request.data['label']
    elif type(request.data) == str:
        reason_text = request.data
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    reason, created = RejectedReason.objects.get_or_create(name=reason_text)
    
    from rejectedProject.models import RejectedProject
    rejected_project = RejectedProject.objects.create(
        name=obj.name,
        client=obj.client,
        last_comment=obj.last_comment or '',
        total=obj.total,
        reason=reason,
    )
    rejected_project.comments.set(obj.comments.all())
    root_price_proposal = obj.root_price_proposal
    obj.delete()
    root_price_proposal.active = False
    root_price_proposal.save()
    rejected_project.root_price_proposal = root_price_proposal
    rejected_project.save()
    
    return Response(status=status.HTTP_200_OK)

