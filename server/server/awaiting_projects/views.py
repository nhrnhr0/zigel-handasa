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
    queryset = AwaitingProject.objects.select_related('client', 'root_price_proposal').all()
    serializer_class = AwaitingProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,multiSelectFilterFactory('root_price_proposal__client__in'),]
    # filterset_fields = ['name','created_at','updated_at',{'alert_date':['lte','gte']},]
    filterset_fields = {
        'name': ['icontains'],
        'created_at': ['lte','gte'],
        'updated_at': ['lte','gte'],
        'alert_date': ['lte','gte'],
    }
    search_fields = ['name','client__name','total','last_comment',]
    pagination_class = StandardResultsSetPagination

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
            'name':{
                'type':'text',
                'name': 'שם',
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
                'type': 'date',
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
            saved_obj.client_id = request.data['client']['value']
            saved_obj.root_price_proposal.client_id = request.data['client']['value']
            saved_obj.root_price_proposal.total = request.data['api_data']['total']
            saved_obj.root_price_proposal.api_data = request.data['api_data']
            saved_obj.root_price_proposal.save()
            saved_obj.comments = request.data['comments']
            saved_obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def awaitingProjectApproveView(request, pk):
    obj = get_object_or_404(AwaitingProject, pk=pk)
    order_number = request.data['order_number']
    root_price_proposal = obj.root_price_proposal
    project = Project.objects.create(
        name=obj.name,
        client=obj.client,
        last_comment=obj.last_comment or '',
        total=obj.total,
        order_number=order_number,
    )
    
    project.comments.set(obj.comments.all())
    
    obj.delete()
    root_price_proposal.active = True
    
    
    project.root_price_proposal = root_price_proposal
    project.save()
    root_price_proposal.project = project
    root_price_proposal.save()
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

