# Generated by Django 2.2.4 on 2019-11-08 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('ipa', models.CharField(blank=True, max_length=50)),
                ('grammar', models.CharField(blank=True, max_length=50)),
                ('definition', models.CharField(blank=True, max_length=50)),
                ('example', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
