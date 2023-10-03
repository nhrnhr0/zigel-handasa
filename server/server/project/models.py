from django.db import models

from base_project.models import BaseProject

class ProjectStatus(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Project(BaseProject):
    status = models.ForeignKey('ProjectStatus', on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=500, null=True, blank=True) # מספר הזמנת רכש
    closed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if self.status_id == None:
            self.status = ProjectStatus.objects.get_or_create(name='חדש')[0]
        super(Project, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-created_at']
        
    def get_total_invoices_before_tax(self):
        root_doc = self.root_price_proposal
        if root_doc is None:
            return 0
        ret = root_doc.get_total_child_invoices_cancelled_calculated()
        return ret