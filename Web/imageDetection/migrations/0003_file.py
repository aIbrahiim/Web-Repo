# Generated by Django 2.2.7 on 2020-02-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('imageDetection', '0002_delete_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
