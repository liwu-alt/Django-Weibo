# Generated by Django 2.1.5 on 2019-02-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190213_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, default='avatar/default.png', upload_to='avatar/%Y/%m/%d/'),
        ),
    ]