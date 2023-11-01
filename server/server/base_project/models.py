from django.db import models

# Create your models here.
class BaseProject(models.Model):
    name = models.CharField(max_length=1000)
    # total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    # docs = models.ManyToManyField('accounting.AccountingDoc', blank=True)
    comments = models.JSONField(null=True, blank=True)
    #last_comment = models.TextField(null=True, blank=True)
    # client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True)
    files= models.ManyToManyField("file_upload.FileUpload")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    root_price_proposal = models.OneToOneField('accounting.AccountingDocPriceProposal', related_name='root_project', on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_last_comment_text(self):
        if self.comments is None:
            return ''
        if len(self.comments) == 0:
            return ''
        return self.comments[0].get('comment', '')
    
    def copy_base_project_data(self, project):
        self.name = project.name
        self.comments = project.comments
        
        self.save()