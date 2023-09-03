from django.contrib import admin
from .models import AccountingDoc
# Register your models here.
class AccountingDocAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'type', 'total')
    list_filter = ('created_at', 'type')
    search_fields = ('name',)
    ordering = ('-created_at',)
admin.site.register(AccountingDoc, AccountingDocAdmin)