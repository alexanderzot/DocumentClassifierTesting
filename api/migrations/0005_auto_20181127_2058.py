# Generated by Django 2.1.3 on 2018-11-27 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20181127_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='owner',
            new_name='user_owner',
        ),
    ]