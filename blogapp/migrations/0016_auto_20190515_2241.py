# Generated by Django 2.2 on 2019-05-15 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0015_auto_20190515_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user_data',
        ),
    ]