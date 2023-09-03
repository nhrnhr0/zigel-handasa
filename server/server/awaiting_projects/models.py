from django.db import models
from base_project.models import BaseProject
# Create your models here.
class   AwaitingProject(BaseProject):
    alert_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-created_at']