from django.contrib import admin
from .models import MsgInfo, UserInfo, UserMsgIndex, HotMsg, Bulletin


@admin.register(MsgInfo)
class MsgInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'type', 'time']
    list_filter = ['time']
    search_fields = ['content', 'user__username']
    date_hierarchy = 'time'


@admin.register(UserMsgIndex)
class UserMsgIndexAdmin(admin.ModelAdmin):
    pass


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']


@admin.register(HotMsg)
class HotMsgAdmin(admin.ModelAdmin):
    list_display = ['title', 'message', 'click_count']

