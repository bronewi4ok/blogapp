# Generated by Django 2.2 on 2019-05-12 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0011_auto_20190512_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newcomment',
            name='from_comment',
        ),
    ]