# Generated by Django 2.2 on 2020-01-14 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0032_post_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='total',
            new_name='price',
        ),
    ]