# Generated by Django 2.2 on 2019-12-23 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0021_auto_20191222_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newcomment',
            name='text',
            field=models.TextField(max_length=900),
        ),
    ]