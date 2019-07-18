from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    birth = models.DateField(blank=True, null=True)
    profile = models.CharField(max_length=32, blank=True, null=True)
    msg_count = models.IntegerField(default=0)
    fans_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    user_status = models.IntegerField(default=0)  # 0：正常，1：锁定
    created = models.DateField(auto_now=True, db_index=True)
    icon = models.ImageField(upload_to='avatar/%Y/%m/%d/', default="avatar/default.jpg", blank=True)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = '用户关系'
        verbose_name_plural = '用户关系'

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following',
                  models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))