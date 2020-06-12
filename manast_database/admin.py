from django.contrib import admin
from manast_database.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    # search_fields = ['']


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('name', 'category', 'shop')
    list_display = ('name', 'category', 'shop')
    # search_fields = ['']


class ExpenseAdmin(admin.ModelAdmin):
    list_filter = ('item', 'shop', 'date')
    list_display = ('shop', 'date')
    ordering = ('-date',)
    # search_fields = ['']


class SalesAdmin(admin.ModelAdmin):
    list_filter = ('item', 'shop', 'date')
    list_display = ('shop', 'date')
    ordering = ('-date',)


# search_fields = ['']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Sale, SalesAdmin)
