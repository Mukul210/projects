# Generated by Django 4.0 on 2021-12-20 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0003_category_sulg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sulg',
            new_name='slug',
        ),
    ]
