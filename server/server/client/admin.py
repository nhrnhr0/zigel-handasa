from django.contrib import admin

from .models import Client
# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','name', )
    list_filter = ('name', )
    search_fields = ('name', )
    ordering = ['name']
admin.site.register(Client, ClientAdmin)