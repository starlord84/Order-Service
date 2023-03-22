from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_datetime', 'user']
    list_display_links = ['order_datetime']


admin.site.register(Organization)
admin.site.register(Dish)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Category)
