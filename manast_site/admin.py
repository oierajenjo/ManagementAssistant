from django.contrib import admin
from manast_site.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('user', 'pk')
    ordering = ('pk', )
    # search_fields = ['']


class ShopAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', 'pk')
    ordering = ('pk', )

# search_fields = ['']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Shop, ShopAdmin)
