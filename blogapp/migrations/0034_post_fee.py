# Generated by Django 2.2 on 2020-01-15 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0033_auto_20200114_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=20),
        ),
    ]
