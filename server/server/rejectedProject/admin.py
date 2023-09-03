from django.contrib import admin
from .models import RejectedReason,RejectedProject

# Register your models here.
class RejectedReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_rejected_projects')
    
    def display_rejected_projects(self, obj):
        return [rejected_project.name for rejected_project in obj.rejected_projects.all()]
    pass
admin.site.register(RejectedReason, RejectedReasonAdmin)
class RejectedProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'last_comment', 'created_at', 'updated_at',)
    pass
admin.site.register(RejectedProject, RejectedProjectAdmin)