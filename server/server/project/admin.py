from django.contrib import admin
from .models import Project, ProjectStatus
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'order_number', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('name', 'order_number')
    ordering = ('-created_at',)
admin.site.register(Project, ProjectAdmin)

class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(ProjectStatus, ProjectStatusAdmin)
