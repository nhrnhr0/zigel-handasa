# Generated by Django 4.2.5 on 2023-09-25 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0004_alter_fileupload_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]