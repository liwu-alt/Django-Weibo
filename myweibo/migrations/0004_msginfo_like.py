# Generated by Django 2.1.5 on 2019-02-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweibo', '0003_comment_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='msginfo',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
