# Generated by Django 2.1.3 on 2018-12-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20181205_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='train_files',
            field=models.ManyToManyField(blank=True, related_name='train_files', to='api.File'),
        ),
    ]
