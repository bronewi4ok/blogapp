# Generated by Django 2.2 on 2020-01-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0028_auto_20200109_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='image/slider/%id')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('caption', models.CharField(blank=True, max_length=50)),
                ('position', models.PositiveIntegerField(default=0, unique=True)),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
