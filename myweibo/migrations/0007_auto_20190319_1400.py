# Generated by Django 2.1.5 on 2019-03-19 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweibo', '0006_auto_20190319_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='content',
            field=models.TextField(max_length=10000),
        ),
    ]
