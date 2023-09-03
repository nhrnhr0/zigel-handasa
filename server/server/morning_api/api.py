import requests

import json
import datetime
import os

def test(request):
    from django.http import JsonResponse

    v = MorningAPI().sync_all_clients()
    return JsonResponse({'data': v})

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class MorningAPI(metaclass=SingletonMeta):
    BASE_MORNING_URL = os.environ['MORNING_API_URL']
    token = None
    expires = None
    def __init__(self):
        print('init morning api')
    
    def make_request(self, url, method='GET', data=None, include_auth=True):
        print('making request', method, ' to ', url)
        if include_auth:
            if not self.token:
                self.refresh_token()
            headers = {
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json'
            }
        else:
            headers = {
                'Content-Type': 'application/json'
            }
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise Exception('Method not supported')
        return response
    
        pass
    def sync_all_clients(self):
        clients = self.get_all_clients_from_morning()
        from client.models import Client #name active taxId paymentTerms phone emails morning_id
        for client in clients:
            client_obj, created = Client.objects.get_or_create(
                morning_id=client['id'],
                defaults={
                    'name': client['name'],
                    'active': client['active'],
                    'taxId': client['taxId'],
                    'paymentTerms': client['paymentTerms'],
                    'phone': client['phone'],
                    'emails': client['emails'],
                }
            )
            if not created:
                client_obj.name = client['name']
                client_obj.active = client['active']
                client_obj.taxId = client['taxId']
                client_obj.paymentTerms = client['paymentTerms']
                client_obj.phone = client['phone']
                client_obj.emails = client['emails']
                client_obj.save()
    def get_all_clients_from_morning(self):
        import time
        print('syncing clients from morning')
        url = f'{self.BASE_MORNING_URL}/clients/search'
        payload = json.dumps({
            "page": 1,
            "active": True,
            "name": "",
            "contactPerson": "",
            "email": "",
            "labels": None
        })
        response = self.make_request(url, method='POST', data=payload)
        # response = requests.post(url, data=payload)
        resp = response.json()
        #         {'pageSize': 25, 'page': 1, 'total': 5, 'from': 1, 'to': 5, 'pages': 1, 'items': [{'id': '9f4b351e-e151-41f0-88e0-2de68fce4e76', 'name': '1234', 'active': True, 'send': True, 'department': '', 'taxId': '319145785', 'accountingKey': '95219739', 'paymentTerms': 30, 'bankName': '', 'bankBranch': '', 'bankAccount': '', 'address': '', 'city': '', 'zip': '', 'country': 'IL', 'phone': '050', 'emails': ['ronionsegal@gmail.com'], 'labels': [], 'remarks': '', 'contactPerson': '', 'incomeAmount': 0, 'paymentAmount': 0, 'creationDate': 1693393943, 'lastUpdateDate': 1693393943, 'balanceAmount': 0, 'self': False}, {'id': 'f389339a-9307-4770-bf72-3f16a3003932', 'name': 'test123', 'active': True, 'send': False, 'department': '', 'taxId': '319145785', 'accountingKey': 'f7980186', 'paymentTerms': 10, 'bankName': '', 'bankBranch': '', 'bankAccount': '', 'address': '', 'city': 
        # '', 'zip': '', 'country': 'IL', 'phone': '052426555544913444', 'emails': [], 'labels': [], 'remarks': '', 'contactPerson': '', 'incomeAmount': 0, 'paymentAmount': 0, 'creationDate': 1693393761, 'lastUpdateDate': 1693393916, 'balanceAmount': 0, 'self': False}, {'id': 'e96569ba-c13a-4bd5-bfe1-83ae83eb9d41', 'name': 'אקדאדדדד', 'active': True, 'send': True, 'department': '', 'taxId': '319145785', 'accountingKey': 'e7647925', 'paymentTerms': 30, 'bankName': '', 'bankBranch': '', 'bankAccount': '', 'address': '', 'city': 
        # '', 'zip': '', 'country': 'IL', 'phone': '0524269134', 'emails': [], 'labels': [], 'remarks': '', 'contactPerson': '', 'incomeAmount': 0, 'paymentAmount': 0, 'creationDate': 
        # 1693465044, 'lastUpdateDate': 1693465044, 'balanceAmount': 0, 'self': False}, {'id': '7a71026d-ca7a-46d1-908e-e052f6a9daba', 'name': 'לקוח מספר 1', 'active': True, 'send': True, 'department': '', 'taxId': '', 'accountingKey': '74012162', 'paymentTerms': 10, 'bankName': 'גכד', 'bankBranch': '234', 'bankAccount': '23423422', 'address': '', 'city': 
        # '', 'zip': '', 'country': 'IL', 'phone': '', 'emails': [], 'labels': [], 'remarks': '', 'contactPerson': '', 'incomeAmount': 8564.87, 'paymentAmount': 8948, 'creationDate': 1692789817, 'lastUpdateDate': 1692865338, 'balanceAmount': 383.13, 'self': False}, {'id': 'f30536c8-8710-4f04-8a3d-435285dd706e', 'name': 'מרי', 'active': True, 'send': True, 
        # 'department': '', 'taxId': '319145785', 'accountingKey': 'f7963292', 'paymentTerms': 90, 'bankName': '', 'bankBranch': '', 'bankAccount': '', 'address': '', 'city': '', 'zip': '', 'country': 'IL', 'phone': '0524269134', 'emails': [], 'labels': [], 'remarks': '', 'contactPerson': '', 'incomeAmount': 0, 'paymentAmount': 0, 'creationDate': 1693463524, 'lastUpdateDate': 1693463524, 'balanceAmount': 0, 'self': False}], 'aggregations': {'totalIncome': {'value': 8564.869999999999}, 'totalPayment': {'value': 8948}, 'byName': {'buckets': []}}}}
        clients = resp['items']
        while resp['page'] < resp['pages']:
            time.sleep(1)
            response = self.make_request(url, method='POST', data=payload)
            resp = response.json()
            clients.extend(resp['items'])
        
        print(clients)
        return clients

    def refresh_token(self):
        print('refreshing token')
        # POST https://sandbox.d.greeninvoice.co.il/api/v1/account/token
        # {
        #   "id": "64e0b4c3-e49c-454d-beb3-060c42c070f8",
        #   "secret": "Tnyu1eqYWB0xEi1oGK29PA"
        #}
        url = f'{self.BASE_MORNING_URL}/account/token'
        data = {
            "id": "64e0b4c3-e49c-454d-beb3-060c42c070f8",
            "secret": "Tnyu1eqYWB0xEi1oGK29PA"
        }
        # response = self.make_request(url, method='POST', data=data, include_auth=False)
        response = requests.post(url, data=data)
        resp = response.json()
        print(resp)
        self.token = resp['token']
        self.expires = resp['expires']
        pass