# Generated by Django 2.2 on 2020-01-08 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0025_auto_20200108_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug_date',
            field=models.SlugField(blank=True, default='abc', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug_title',
            field=models.SlugField(blank=True, default='abc', max_length=200, null=True),
        ),
    ]
