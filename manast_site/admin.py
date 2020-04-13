from django.contrib import admin
from manast_site.models import *


class ProfileAdmin(admin.ModelAdmin):
    # list_filter = ('',)
    list_display = ('user', 'pk')
    # search_fields = ['']


admin.site.register(Profile, ProfileAdmin)

