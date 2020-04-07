# Generated by Django 2.2.3 on 2019-07-29 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storytime', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='original_author',
            new_name='adaptation_author',
        ),
        migrations.RenameField(
            model_name='story',
            old_name='original_source',
            new_name='original_source_title',
        ),
        migrations.AddField(
            model_name='story',
            name='original_source_author',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
    ]
