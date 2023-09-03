from django.db import models

# Create your models here.

FINANCIAL_DOC_TYPES = (
    (10, 'הצעת מחיר'),
    (305, 'חשבונית מס'),
    (330, 'חשבונית זיכוי'),
    (400, 'קבלה'),
)


FINANCIAL_DOC_TYPES_DICT = {
    10: 'הצעת מחיר',
    305: 'חשבונית מס',
    330: 'חשבונית זיכוי',
    400: 'קבלה',
}


class AccountingDoc(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    doc_number = models.CharField(max_length=50, null=True, blank=True)
    base_price_proposal = models.ForeignKey('AccountingDocPriceProposal', on_delete=models.SET_NULL, null=True, blank=True, related_name='docs')
    type = models.IntegerField(choices=FINANCIAL_DOC_TYPES)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    api_data = models.JSONField(null=True, blank=True)
    morning_id = models.CharField(max_length=500, null=True, blank=True)
    based_on = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='based_docs')
    
    class Meta:
        ordering = ['-created_at']
    def get_type_display(self):
        return FINANCIAL_DOC_TYPES_DICT[self.type]
    def __str__(self):
        return f"{FINANCIAL_DOC_TYPES_DICT[self.type]}: {self.total}"


class AccountingDocPriceProposal(AccountingDoc):
    pass
class AccountingDocInvoice(AccountingDoc):
    pass
class AccountingDocReceipt(AccountingDoc):
    pass
