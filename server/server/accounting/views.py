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
from accounting.models import AccountingDoc, AccountingDocInvoice
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(["GET"])
def get_accounting_docs_morning_info(request):
    morning_ids = request.GET.get('morning_ids[]')
    morning_ids = morning_ids.split(',')
    from accounting.models import AccountingDoc
    docs = AccountingDoc.objects.filter(morning_id__in=morning_ids)
    return JsonResponse({'docs':AccountingDocDetailSerializer(docs,many=True).data})

@api_view(["POST"])
def create_invoice_from_price_proposals(request):
    from morning_api.api import MorningAPI
    
    clientDict = request.data.get('client')
    date = request.data.get('date') # '2023-09-10T21:00:00.000Z'
    due_date = request.data.get('dueDate') #'2023-10-30T22:00:00.000Z'
    income = request.data.get('income')
    remarks = request.data.get('remarks')
    fotter = request.data.get('fotter')
    emailContent = request.data.get('emailContent')
    description = request.data.get('description')
    discount = request.data.get('discount')
    subtotal = request.data.get('subtotal')
    total = request.data.get('total')
    # convert date to morning format:   "date": "2017-10-03",
    date = MorningAPI().convert_django_date_to_morning_date(date)
    due_date = MorningAPI().convert_django_date_to_morning_date(due_date)
    

    response = MorningAPI().create_invoice_from_price_proposals(clientDict, date, due_date, income, remarks, fotter, emailContent,description,discount)
    if not response.ok:
        return JsonResponse({'error':response.json()['errorMessage']})
    
    # create AccountingDocInvoice object 
    linkedDocumentIds = request.data.get('linkedDocumentIds')
    morning_id = response.json()['id']
    client = Client.objects.get(morning_id=clientDict['id'])
    
    invoice = AccountingDocInvoice.objects.create(client=client, type=305, morning_id=morning_id, doc_number=response.json()['number'], api_data=response.json())
    # set rootPriceProposals
    root_price_proposals = []
    based_on = []
    for linkedDocumentId in linkedDocumentIds:
        price_prop = AccountingDoc.objects.get(morning_id=linkedDocumentId)
        root_price_proposals.extend(price_prop.root_price_proposals.all())
        based_on.append(price_prop)
    root_price_proposals = list(set(root_price_proposals))
    invoice.root_price_proposals.set(root_price_proposals)
    buckets = []
    for price_prop in based_on:
        buckets.append({
            'id': price_prop.morning_id,
            'max': int(price_prop.get_open_amount()),
            'total': 0,
        })
    
    buckets.sort(key=lambda x: x['max'])
    has_space = False
    remaining_total = remove_tax(total)
    idx= 0
    while remaining_total > 0:
        # check if there are any spaces left
        has_space = False
        for bucket in buckets:
            if bucket['max'] > bucket['total']:
                has_space = True
                break
        if not has_space:
            break
            
        while buckets[idx % len(buckets)]['max'] <= buckets[idx % len(buckets)]['total']:
            idx += 1
        buckets[idx % len(buckets)]['total'] += 1
        remaining_total -= 1
        idx += 1
        
    if remaining_total > 0:
        # split the remaining total between all buckets evenly
        for bucket in buckets:
            bucket['total'] +=  int(remaining_total / len(buckets))
    # for each bucket create a Relation object
    for bucket in buckets:
        from accounting.models import AccountingDocRelation
        parent = AccountingDoc.objects.get(morning_id=bucket['id'])
        AccountingDocRelation.objects.create(parent=parent, child=invoice, total=bucket['total'])
    # update invoice total
    invoice.total = total
    invoice.save()
    return JsonResponse({'data':response.json()})
    pass

def remove_tax(total):
    from decimal import Decimal
    if isinstance(total, str):
        total = Decimal(total)
    return int(total / Decimal(1.17))