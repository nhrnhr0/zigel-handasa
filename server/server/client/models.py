from django.db import models
#{"id": "9f4b351e-e151-41f0-88e0-2de68fce4e76","name": "1234","active": true,"send": true,"department": "","taxId": "319145785","accountingKey": "95219739","paymentTerms": 30,"bankName": "","bankBranch": "","bankAccount": "","address": "","city": "","zip": "","country": "IL","phone": "050","emails": ["ronionsegal@gmail.com"],"labels": [],"remarks": "","contactPerson": "","incomeAmount": 0,"paymentAmount": 0,"creationDate": 1693393943,"lastUpdateDate": 1693393943,"balanceAmount": 0,"self": false},{"id": "f389339a-9307-4770-bf72-3f16a3003932","name": "test123","active": true,"send": false,"department": "","taxId": "319145785","accountingKey": "f7980186","paymentTerms": 10,"bankName": "","bankBranch": "","bankAccount": "","address": "","city": "","zip": "","country": "IL","phone": "052426555544913444","emails": [],"labels": [],"remarks": "","contactPerson": "","incomeAmount": 0,"paymentAmount": 0,"creationDate": 1693393761,"lastUpdateDate": 1693393916,"balanceAmount": 0,"self": false},# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    taxId = models.CharField(max_length=100, blank=True)
    paymentTerms = models.IntegerField(default=0)
    phone = models.CharField(max_length=100, blank=True)
    emails = models.JSONField(default=list)
    morning_id = models.CharField(max_length=100, blank=True)
    morning_last_update = models.DateTimeField(auto_now=True)
    api_data = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"
    
    def get_data(self):
        if self.api_data is None:
            return {}
        return self.api_data