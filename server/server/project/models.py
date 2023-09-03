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
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if self.status_id == None:
            self.status = ProjectStatus.objects.get_or_create(name='חדש')[0]
        super(Project, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-created_at']