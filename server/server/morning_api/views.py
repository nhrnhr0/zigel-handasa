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
    from accounting.models import FINANCIAL_DOC_TYPES, AccountingDocPriceProposal,AccountingDocReceipt,AccountingDoc,AccountingDocRelation
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
                
                # conver alert_date to datetime object
                alert_date = datetime.combine(alert_date, datetime.min.time())
                
                # set timezone to Asia/Jerusalem
                from django.utils.timezone import make_aware
                import pytz
                alert_date = make_aware(alert_date, timezone=pytz.timezone("Asia/Jerusalem"))
                
                
                # if price_proposal_created and api_data has no 'discount' object, we add it
                # "discount": {
                #     "total": "0.00",
                #     "type": "amount",
                #     "value": ""
                # },
                if not price_proposal.api_data.get('discount'):
                    price_proposal.api_data['discount'] = {
                        "total": "0.00",
                        "type": "amount",
                        "value": ""
                    }
                    
                # set "tax": [{total: convert to string}] with 2 decimals
                # and api_data.total to string with 2 decimals
                x = float(price_proposal.api_data['tax'][0]['total'])
                price_proposal.api_data['tax'][0]['total'] = f"{x:.2f}"
                x = float(price_proposal.api_data['total'])
                price_proposal.api_data['total'] = f"{x:.2f}"
                awaiting_project = AwaitingProject.objects.create(name=request.data['description'],root_price_proposal=price_proposal,alert_date=alert_date)
                price_proposal.root_price_proposals.add(price_proposal) # add self to root price proposals so serializer will work doc.root_price_proposals.all()__root_project__name

                price_proposal.save()
    #{'id': '8292f9c1-0681-421c-a...3f7775b021', 'type': 400, 'number': 80011, 'currency': 'ILS', 'date': '2023-09-12', 'createdAt': 1695018103000, 'subtotal': 0, 'rounding': False, 'tax': [{...}], 'total': 2000, 'description': 'פרויקט 1', 'remarks': 'קבלה עבור חשבונית מס 50038', 'reverseCharge': False, 'recipient': {'id': '7a71026d-ca7a-46d1-9...52f6a9daba', 'name': 'לקוח מספר 1', 'department': '', 'address': '', 'city': '', 'zip': '', 'country': 'IL', 'phone': '', 'mobile': '', ...}, ...}
    elif(request.data['type'] == 400):
        client_morning_id =request.data['recipient'].get('id', None)
        client = None
        if client_morning_id:
            client,client_created = Client.objects.get_or_create(morning_id=client_morning_id)
        if client:
            # we need to get or create the receipt
            receipt, receipt_created = AccountingDocReceipt.objects.get_or_create(morning_id=request.data['id'],
                                                                                                      defaults={
                                                                                                          'client':client,
                                                                                                          'active':False,
                                                                                                          'doc_number':request.data['number'],
                                                                                                          'type':request.data['type'],
                                                                                                          'total':request.data['total'],
                                                                                                          'api_data':request.data})

            if receipt_created:
                root_price_proposals = []
                linked_docs = MorningAPI().get_linked_docs(request.data['id'])
                if linked_docs.ok == True:
                    linked_docs = linked_docs.json()
                    print(linked_docs)
                    total_per_child = receipt.total_before_tax / len(linked_docs)
                    for doc in linked_docs:
                        doc_id = doc['id']
                        doc = AccountingDoc.objects.filter(morning_id=doc_id).first()
                        if doc:
                            rel = AccountingDocRelation.objects.create(parent=doc,child=receipt, total=total_per_child)
                            root_price_proposals.extend(doc.root_price_proposals.all())
                            rel.save()
                receipt.active = True
                receipt.root_price_proposals.set(root_price_proposals)
                receipt.save()

    return HttpResponse('ok', status=200)




    pass