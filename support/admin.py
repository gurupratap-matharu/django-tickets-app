from django.contrib import admin

from .models import Holiday, Vendor, Category, Ticket

admin.site.register(Holiday)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Ticket)
