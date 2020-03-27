from django.contrib import admin
from manasis_site.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    # list_filter = ('',)
    list_display = ('user', 'pk')
    # search_fields = ['']


admin.site.register(Profile, ProfileAdmin)
