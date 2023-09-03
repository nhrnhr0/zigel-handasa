from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RejectedReasonSelectSerializer
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
class RejectedReasonSelectView(generics.ListAPIView):
    """
    View to list all rejected reasons in the system.

    * Requires token authentication.
    """
    queryset = RejectedReason.objects.all()
    serializer_class = RejectedReasonSelectSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    
    
class RejectedProjectListView(generics.ListAPIView):
    queryset = RejectedProject.objects.select_related('client', 'reason').all()
    serializer_class = RejectedProjectSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,ClientMultiSelectFilter,ReasonMultiSelectFilter]
    filterset_fields = ['name','client','reason','created_at','updated_at',]
    search_fields = ['name','client__name','last_comment','reason__name',]
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
            'reason__name': {
                'lable': 'סיבה',
                'sortable': True,
                'type': 'text',
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
