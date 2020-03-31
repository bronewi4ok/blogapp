# Generated by Django 2.2 on 2020-01-16 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200116_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('created', 'Created'), ('hipped', 'Shipped'), ('refaunded', 'Refaunded')], default='created', max_length=120),
        ),
    ]