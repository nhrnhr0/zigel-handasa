from django.db import models
from base_project.models import BaseProject
# Create your models here.
class RejectedReason(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.name}"

class RejectedProject(BaseProject):
    reason = models.ForeignKey('RejectedReason', on_delete=models.SET_NULL, null=True, related_name='rejected_projects')
    def __str__(self):
        return f"{self.name}: {self.reason}"
    