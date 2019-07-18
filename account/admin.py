from django.contrib import admin
from .models import Profile, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fans_count', 'follow_count', 'msg_count', 'sex', 'birth', 'profile']
    search_fields = ['user__username', 'profile']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']


admin.site.site_header = '微博管理系统'
admin.site.site_title = '微博管理'



