from django.db import models

# Create your models here.
class BaseProject(models.Model):
    name = models.CharField(max_length=1000)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    # docs = models.ManyToManyField('accounting.AccountingDoc', blank=True)
    comments = models.ManyToManyField('comment.Comment', blank=True)
    last_comment = models.TextField(null=True, blank=True)
    client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    root_price_proposal = models.OneToOneField('accounting.AccountingDocPriceProposal', related_name='root_project', on_delete=models.SET_NULL, null=True, blank=True)
    