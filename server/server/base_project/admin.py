from django.contrib import admin
from .models import BaseProject
# Register your models here.
class BaseProjectAdmin(admin.ModelAdmin):
    list_display = ('name','root_price_proposal','created_at','updated_at',)
    search_fields = ('name',)
    ordering = ('-created_at',)
admin.site.register(BaseProject, BaseProjectAdmin)