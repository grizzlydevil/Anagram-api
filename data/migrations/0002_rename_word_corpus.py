# Generated by Django 4.0.5 on 2022-06-03 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Word',
            new_name='Corpus',
        ),
    ]
