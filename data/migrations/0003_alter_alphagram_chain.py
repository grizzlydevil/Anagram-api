# Generated by Django 4.0.5 on 2022-06-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_rename_word_corpus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alphagram',
            name='chain',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]