# Generated by Django 2.2 on 2019-11-07 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0016_auto_20190515_2241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_date']},
        ),
    ]
