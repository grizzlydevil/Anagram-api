# Generated by Django 4.0.5 on 2022-06-06 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_alter_corpus_hash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corpus',
            name='alphagram',
        ),
        migrations.DeleteModel(
            name='Alphagram',
        ),
    ]