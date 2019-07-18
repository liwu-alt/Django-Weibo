# Generated by Django 2.1.5 on 2019-02-15 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MsgInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=512)),
                ('type', models.IntegerField(default=0)),
                ('commented_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('transferred_count', models.IntegerField(default=0)),
                ('transfer_count', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now=True, db_index=True)),
                ('Content_img', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_create', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='msg_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'MicroBlog',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_count', models.IntegerField(default=0)),
                ('fans_count', models.IntegerField(default=0)),
                ('follow_count', models.IntegerField(default=0)),
                ('user_status', models.IntegerField(default=0)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMsgIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweibo.MsgInfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_index', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]