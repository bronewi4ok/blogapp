# Generated by Django 2.2 on 2019-05-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190515_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='/media/avaratrs/noavatar.png', null=True, upload_to='avatars/'),
        ),
    ]
