# Generated by Django 2.1.5 on 2019-02-17 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweibo', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(default=None, max_length=8),
        ),
    ]
