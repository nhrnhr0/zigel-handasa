from django.contrib import admin
from .models import Navbar
# Register your models here.
class NavbarAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order')
    list_filter = ('name', 'url', 'order')
    search_fields = ('name', 'url', 'order')
    ordering = ['order']
admin.site.register(Navbar, NavbarAdmin)