from django.contrib import admin
from .models import AccountingDoc,AccountingDocRelation
# Register your models here.
class AccountingDocAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'type', 'total')
    list_filter = ('created_at', 'type')
    search_fields = ('name',)
    ordering = ('-created_at',)
admin.site.register(AccountingDoc, AccountingDocAdmin)

class AccountingDocRelationAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child', 'total')
    
admin.site.register(AccountingDocRelation, AccountingDocRelationAdmin)