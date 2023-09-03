from django.contrib import admin
from .models import AwaitingProject
# Register your models here.
class AwaitingProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', )
    list_filter = ('name', )
    search_fields = ('name', )
    ordering = ['name']
admin.site.register(AwaitingProject, AwaitingProjectAdmin)