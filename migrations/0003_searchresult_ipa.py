# Generated by Django 2.2.4 on 2019-11-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notemaker', '0002_searchresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='ipa',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
