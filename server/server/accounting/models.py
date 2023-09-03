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
    type = models.IntegerField(choices=FINANCIAL_DOC_TYPES)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    api_data = models.JSONField(null=True, blank=True)
    morning_id = models.CharField(max_length=500, null=True, blank=True, unique=True)
    childs = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='parent_docs')
    root_price_proposals = models.ManyToManyField('accounting.AccountingDocPriceProposal', blank=True, related_name='child_docs')
    
    is_root_doc = property(lambda self: self.childs.count() > 0)

    
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
