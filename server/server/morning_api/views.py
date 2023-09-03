from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from morning_api.api import MorningAPI
from django.http import HttpResponse
@csrf_exempt
@api_view(["POST"])
def morningWebhookClientView(request):
    MorningAPI().sync_all_clients()
    return HttpResponse('ok', status=200)


@csrf_exempt
@api_view(["POST"])
def morningWebhookDocumentView(request):
    from accounting.models import FINANCIAL_DOC_TYPES, AccountingDocPriceProposal
    from client.models import Client
    from awaiting_projects.models import AwaitingProject
    from datetime import datetime, timedelta
    # request.data['type']:10
    # check if doc type is in FINANCIAL_DOC_TYPES
    # if not, return
    if request.data['type'] not in [x[0] for x in FINANCIAL_DOC_TYPES]:
        return HttpResponse('ok', status=200)
    

            
    if(request.data['type'] == 10):
        client_morning_id =request.data['recipient'].get('id', None)
        client = None
        if client_morning_id:
            client,client_created = Client.objects.get_or_create(morning_id=client_morning_id)
        if client:
            # we need to get or create the price proposal
            price_proposal, price_proposal_created = AccountingDocPriceProposal.objects.get_or_create(morning_id=request.data['id'],
                                                                                                      defaults={
                                                                                                          'client':client,
                                                                                                          'active':False,
                                                                                                          'doc_number':request.data['number'],
                                                                                                          'type':request.data['type'],
                                                                                                          'total':request.data['total'],
                                                                                                          'api_data':request.data})
            
            if price_proposal_created:
                # we need to create the awaiting project, set the alert date 7 days from now
                alert = request.data['date']
                alert_date = datetime.strptime(alert, '%Y-%m-%d')
                alert_date = alert_date.date() + timedelta(days=7)
                
                awaiting_project = AwaitingProject.objects.create(name=request.data['description'],root_price_proposal=price_proposal,alert_date=alert_date, client=client, total=request.data['total'])
                price_proposal.root_price_proposals.add(price_proposal) # add self to root price proposals so serializer will work doc.root_price_proposals.all()__root_project__name

                price_proposal.save()

    
    return HttpResponse('ok', status=200)




    pass