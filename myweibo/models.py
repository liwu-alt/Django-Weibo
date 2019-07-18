from django.db import models
from django.conf import settings


# 此表已经弃用 将其相关字段放在account profile表中
class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    msg_count = models.IntegerField(default=0)
    fans_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    user_status = models.IntegerField(default=0)  # 0：正常，1：锁定
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return "Info_count for user {}".format(self.user.username)


class MsgInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='msg_create', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    type = models.IntegerField(default=0)
    commented_count = models.IntegerField(default=0)  # 评论过的数量，只增不减
    comment_count = models.IntegerField(default=0)  # 保留的评论数量
    transferred_count = models.IntegerField(default=0)  # 转发过的数量，只增不减
    transfer_count = models.IntegerField(default=0)  # 保留的转发数量
    time = models.DateTimeField(auto_now=True, db_index=True)
    Content_img = models.ImageField(upload_to='images/%Y/%m/%d',
                                    null=True, blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='msg_liked', blank=True)
    like = models.IntegerField(default=0)

    class Meta:
        verbose_name = '微博消息'
        verbose_name_plural = '微博消息'


class UserMsgIndex(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='msg_index',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    message = models.ForeignKey(MsgInfo, on_delete=models.CASCADE)
    time = models.DateTimeField()

    class Meta:
        verbose_name = '用户消息索引'
        verbose_name_plural = '用户消息索引'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=8, default=user.name)
    content = models.CharField(max_length=140)
    message = models.ForeignKey(MsgInfo, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)


class HotMsg(models.Model):
    title = models.CharField(max_length=32)
    message = models.ForeignKey(MsgInfo, on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = '热门微博'
        verbose_name_plural = '热门微博'


class Bulletin(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField(max_length=10000)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
