# Generated by Django 2.2 on 2020-01-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oorder_id',
            new_name='order_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('created', 'Created'), ('hipped', 'Shipped'), ('refaunded', 'Refaunded')], default='created', max_length=120),
        ),
    ]