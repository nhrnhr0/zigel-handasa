# Generated by Django 4.2.4 on 2023-09-05 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_project', '0004_remove_baseproject_comments_baseproject_comments'),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
