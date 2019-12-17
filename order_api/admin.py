from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.


class OrderAdmin(admin.ModelAdmin):

    fields = ['owner', 'contact', 'items']
    list_display = ['order_uid', 'ts', 'owner', 'contact']


class ContactAdmin(admin.ModelAdmin):

    fields = ['order', 'phone', 'address', 'full_name', 'contact_email', 'items' ]


class ItemAdmin(admin.ModelAdmin):

    fields = ['name', 'price', 'description']


admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.unregister(Group)