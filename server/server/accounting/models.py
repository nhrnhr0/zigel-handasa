from django.db import models
from decimal import Decimal
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

# through class for m2m relationship between the parents docs and the docs that are related to them
class AccountingDocRelation(models.Model):
    parent = models.ForeignKey('accounting.AccountingDoc', on_delete=models.CASCADE, related_name='childs')
    child = models.ForeignKey('accounting.AccountingDoc', on_delete=models.CASCADE, related_name='parents')
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    class Meta:
        unique_together = ('parent', 'child')

class AccountingDoc(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    doc_number = models.CharField(max_length=50, null=True, blank=True)
    type = models.IntegerField(choices=FINANCIAL_DOC_TYPES)
    
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    total_before_tax = property(lambda self: int(self.total / Decimal(1.17)))
    created_at = models.DateTimeField(auto_now_add=True)
    api_data = models.JSONField(null=True, blank=True)
    morning_id = models.CharField(max_length=500, null=True, blank=True, unique=True)
    root_price_proposals = models.ManyToManyField('accounting.AccountingDocPriceProposal', blank=True, related_name='child_docs')
    # based_on = models.ManyToManyField('self', blank=True, through='accounting.AccountingDocRelation', symmetrical=False, related_name='related_to')
    
    is_root_doc = property(lambda self: self.childs.count() > 0)

    def get_open_amount(self):
        
        if self.type == 10:# price proposal
            return self.total_before_tax - self.get_total_child_invoices()
        elif self.type == 305:# invoice
            return self.total_before_tax - self.get_total_child_receipts()
        
    def get_total_child_invoices(self):
        return self.get_total_child_docs_by_type(305)
    
    def get_total_child_receipts(self):
        return self.get_total_child_docs_by_type(330)
    def get_total_child_docs_by_type(self, type):
        total = 0
        for child_rel in self.childs.all():
            if child_rel.child.type == type:
                total += child_rel.total
        return total
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
