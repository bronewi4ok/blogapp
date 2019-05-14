# Generated by Django 2.2 on 2019-05-11 20:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_auto_20190511_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blogapp.NewComment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_comments', to='blogapp.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
